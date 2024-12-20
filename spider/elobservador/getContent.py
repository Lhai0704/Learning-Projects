import requests
import pandas as pd
from datetime import datetime
import time
from typing import Optional, Dict, Tuple
import logging
import json
from bs4 import BeautifulSoup
import re


class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/xml',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',  # Do Not Track
        }

        self.cookies: Dict[str, str] = {
            'cf_clearance': 'EunFb5muCkePLK6LI_Bkrf1DWs_IGpuPm.aXrJOWv.8-1734669787-1.2.1.1-O.9UQvXnBwqLn2qG6IURPgqmjV2_q2572DTIn.liuV6pFKwI4XVK6VIfSQck9fowtX.d7bNJ8yJHRAupHrojdv3FdwH2POevXEVi.2pBdS9dciuH7vusB8aaSCBXEkMd_.sz7IyRqEBq1KuJaNVofokeL8tNh0HrklO3BfISn6gNqPxdVMYAM7owLizKH1NYe1avMsT_qqIzgfVJ3ZvJxkMzn7P_6l_PRir1kad5bZczsW8qvssJNYlf4Qhl1KAp_ugtyfy_ikXZ7DKBI4tD6TTzbH6lePa9AXhpMang0C78hNw3.jMPfCwhYcovHrk8ZFdZyjJRKcHdKaTRE_UMUIxNiNO.fUw5KYkXWh1oJW1.MmJdBFe31MPWw8JCuiuIvPq9HnLTziJ.17yyyKkJ6XVppueRf53c3npVWd6aL8NZL.7pefwfgfP_szqS.1Wb',
        }

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url: str, retry_times: int = 3) -> Optional[str]:
        """获取网页内容"""
        for i in range(retry_times):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=10
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                self.logger.error(f"第 {i + 1} 次请求失败: {url}")
                self.logger.error(f"错误信息: {str(e)}")
                if i == retry_times - 1:
                    self.logger.error(f"达到最大重试次数，放弃请求: {url}")
                    return None
                time.sleep(2 ** i)
        return None

    def extract_json_ld(self, html: str) -> Tuple[Optional[str], Optional[str]]:
        """从JSON-LD中提取标题和正文"""
        try:
            # 使用正则表达式找到JSON-LD部分
            json_ld_match = re.search(r'<script type="application/ld\+json".*?>(.*?)</script>', html, re.DOTALL)
            if not json_ld_match:
                return None, None

            json_data = json.loads(json_ld_match.group(1))

            # 处理可能的数组情况
            if isinstance(json_data, list):
                json_data = json_data[0]

            title = json_data.get('name')
            content = json_data.get('articleBody')

            return title, content
        except (json.JSONDecodeError, AttributeError) as e:
            self.logger.error(f"解析JSON-LD时出错: {str(e)}")
            return None, None

    def extract_category(self, html: str) -> Optional[str]:
        """从breadcrumb中提取分类"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            breadcrumb = soup.find('div', class_='main-header_breadcrumb')

            if not breadcrumb:
                return None

            # 获取所有链接文本和最后的文本节点
            categories = []

            # 获取所有链接中的文本
            for link in breadcrumb.find_all('a', class_='news-headline__topic-link'):
                text = link.get_text(strip=True)
                if text:
                    categories.append(text)

            # 获取最后一个文本节点
            last_text = breadcrumb.contents[-1]
            if isinstance(last_text, str):
                last_category = last_text.strip().strip('/')
                if last_category:
                    categories.append(last_category)

            return '/'.join(categories) if categories else None

        except Exception as e:
            self.logger.error(f"提取分类时出错: {str(e)}")
            return None

    def process_csv(self, input_path: str, output_path: str):
        """处理CSV文件"""
        try:
            # 读取CSV文件
            df = pd.read_csv(input_path)

            # 确保必要的列存在
            if 'url' not in df.columns or 'date' not in df.columns:
                raise ValueError("CSV必须包含'url'和'date'列")

            # 添加新列
            if 'title' not in df.columns:
                df['title'] = None
            if 'content' not in df.columns:
                df['content'] = None
            if 'category' not in df.columns:
                df['category'] = None
            if 'fetch_status' not in df.columns:
                df['fetch_status'] = None
            if 'fetch_time' not in df.columns:
                df['fetch_time'] = None

            # 处理每个URL
            for index, row in df.iterrows():
                self.logger.info(f"处理第 {index + 1} 条记录: {row['url']}")

                html_content = self.fetch_page(row['url'])
                if html_content:
                    # 提取标题和正文
                    title, article_body = self.extract_json_ld(html_content)
                    # 提取分类
                    category = self.extract_category(html_content)

                    df.at[index, 'title'] = title
                    df.at[index, 'content'] = article_body
                    df.at[index, 'category'] = category
                    df.at[index, 'fetch_status'] = 'success'
                else:
                    df.at[index, 'fetch_status'] = 'failed'

                df.at[index, 'fetch_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 每处理10条记录保存一次
                if (index + 1) % 10 == 0:
                    df.to_csv(output_path, index=False)
                    self.logger.info(f"保存进度: {index + 1} 条记录")

                time.sleep(1)  # 避免请求过于频繁

            # 最终保存
            df.to_csv(output_path, index=False)
            self.logger.info("处理完成")

        except Exception as e:
            self.logger.error(f"处理CSV文件时发生错误: {str(e)}")
            raise


def main():
    # 使用示例
    scraper = WebScraper()

    # 测试单个URL
    # test_url = "https://www.elobservador.com.uy/nota/lacalle-participo-de-entrega-de-campos-de-colonizacion-con-ausencias-de-senadores-blancos-2021112712182"
    # html_content = scraper.fetch_page(test_url)
    # if html_content:
    #     # 测试提取标题和正文
    #     title, content = scraper.extract_json_ld(html_content)
    #     print("标题:", title)
    #     print("正文前1000个字符:", content[:1000] if content else None)
    #
    #     # 测试提取分类
    #     category = scraper.extract_category(html_content)
    #     print("分类:", category)
    # else:
    #     print("获取内容失败")

    # 如果要处理CSV文件，取消下面的注释
    scraper.process_csv('hong-kong.csv', 'hong-kong-data.csv')


if __name__ == "__main__":
    main()