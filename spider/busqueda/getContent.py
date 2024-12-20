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
            'cf_clearance': 'gNvgHd58k2sdPr2RmAnb70lJhLw0zDLB2y39nzUfYwM-1734674230-1.2.1.1-ZW0zES9Wh1gssanAIJUkSNr.ZfUEfRt_hg5oldm25q2tKHBbYynfCa.z0m092OyS7yE747MeSFnGU9qzLxY1H2FPAqcxCTpZY0hQLMZqceV2yCl_zCWG3mLT0ENQQFbDIOPm02wwdA2ZDPf10jaZ_xrwV7UbP_ihxLTXARNYJKIb.TmZOOvGseXM1uCBayZxCfwtGPi57iwDmvQnPg1oM6EUzaugaz5WvDbnlhFOxTreMFHOS5yroXH7y0AR4_GO85ziSZpBJJmhU2zmfiBJYolcJAImEZR9p64CP4GR2d3WMMatnCPtroAD.YYq6Ql72.MRLFIPpwbLbYe5H4SX7_XoCwcBYsDJFVvt.6ZY115KqDHqfsaN.bzDg17XJ4hhXsZx5Dn9TBx8nkO4kAUIr8eA0QHBFWA.TYq0kRF4Hc3oU9sLOosP.JKWaQFx3c1p',
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

    # def extract_json_ld(self, html: str) -> Tuple[Optional[str], Optional[str]]:
    #     """从JSON-LD中提取标题和正文"""
    #     try:
    #         # 使用更宽松的正则表达式来匹配JSON-LD部分
    #         json_ld_match = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
    #         if not json_ld_match:
    #             return None, None
    #
    #         # 清理JSON数据中可能存在的转义字符
    #         json_str = json_ld_match.group(1)
    #         json_str = json_str.replace('\\"', '"').replace('\\/', '/')
    #
    #         json_data = json.loads(json_str)
    #
    #         # 处理可能的数组情况
    #         if isinstance(json_data, list):
    #             json_data = json_data[0]  # 取第一个元素
    #
    #         # 提取字段
    #         title = json_data.get('name', '').strip()
    #         content = json_data.get('articleBody', '').strip()
    #
    #         return title, content
    #     except (json.JSONDecodeError, AttributeError) as e:
    #         self.logger.error(f"解析JSON-LD时出错: {str(e)}")
    #         return None, None

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

    # def extract_category(self, html: str) -> Optional[str]:
    #     """从breadcrumb中提取分类"""
    #     try:
    #         soup = BeautifulSoup(html, 'html.parser')
    #         breadcrumb = soup.find('div', class_='main-header_breadcrumb')
    #
    #         if not breadcrumb:
    #             return None
    #
    #         # 获取所有链接文本和最后的文本节点
    #         categories = []
    #
    #         # 获取所有链接中的文本
    #         for link in breadcrumb.find_all('a', class_='news-headline__topic-link'):
    #             text = link.get_text(strip=True)
    #             if text:
    #                 categories.append(text)
    #
    #         # 获取最后一个文本节点
    #         last_text = breadcrumb.contents[-1]
    #         if isinstance(last_text, str):
    #             last_category = last_text.strip().strip('/')
    #             if last_category:
    #                 categories.append(last_category)
    #
    #         return '/'.join(categories) if categories else None
    #
    #     except Exception as e:
    #         self.logger.error(f"提取分类时出错: {str(e)}")
    #         return None

    def extract_category(self, html: str) -> Optional[str]:
        try:
            # 解析 HTML
            soup = BeautifulSoup(html, 'html.parser')

            # 查找所有的 topic 项
            topics = soup.select('.news-headline__topic-item')

            # 提取并过滤掉 'Búsqueda'，只保留其他的 topic
            result = []
            for topic in topics:
                # 如果是 <a> 标签，获取链接文本
                if topic.find('a'):
                    result.append(topic.find('a').get_text(strip=True))
                # 如果是 <span> 标签，获取文本
                elif topic.find('span'):
                    result.append(topic.find('span').get_text(strip=True))

            # 去掉列表中的 'Búsqueda'（如果有）
            # result = [item for item in result if item != 'Búsqueda']

            # 将结果转换为字符串
            result_str = '/'.join(result)
            return result_str
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

    # # 测试单个URL
    # test_url = "https://www.busqueda.com.uy/Secciones/China-propuso-un-acuerdo-de-cooperacion-en-economia-digital-que-en-Industria-provoca-dudas-uc56139"
    # html_content = scraper.fetch_page(test_url)
    # if html_content:
    #     # 测试提取标题和正文
    #     title, content = scraper.extract_json_ld(html_content)
    #     print("标题:", title)
    #     print("正文字符:", content if content else None)
    #
    #     # 测试提取分类
    #     category = scraper.extract_category(html_content)
    #     print("分类:", category)
    # else:
    #     print("获取内容失败")

    # 如果要处理CSV文件，取消下面的注释
    scraper.process_csv('data/url+time/china.csv', 'data/china_data.csv')


if __name__ == "__main__":
    main()