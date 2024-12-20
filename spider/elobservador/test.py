import requests
import pandas as pd
from datetime import datetime
import time
from typing import Optional, Dict
import logging


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

        # 这里可以添加你的cookies
        self.cookies: Dict[str, str] = {
            'cf_clearance': 'OqZmv3ViqbW8cNcorGCRl9P4jbK8AKHjowLgZdCeaj0-1734657575-1.2.1.1-kf0lmh36Ge.wwiHMjazCJoJMrLJQf.Pqu99VzizPi4fztNDzkikQo1zZQ6hK7yaaRKymFpMUPnL74AzJxCqYLs1jY9K06d.tL3LVwEtU.D76YzttsR4QB2f5qOt7kgmhP5KBTUdfx1Hpjc.CGTGCTaVjJCsoyFG3XLYZbmQo2_IpO96TZawJf5mLUkhBZrVcJ7aPwAeLilpgTa19.5uIdeKCxfia2e3JvumSFuh59iWnVJO4EUwVe6Vmbw67s2uWDl4y5y1cgak7sJ_M4dQ.b8yViu7aGIIRBPw8zH_ie1OAQbYsCibB1XjpTaxgcKv.vok9KJvhcWr_DwaUibl2HELoZtnKyDESpQxNPwUhGqSSriFp_zP2vgvvf3In9NOGntNpevNnq8N98o8hFGkAWje0uUTLAJpopyFO9fOkh1uD4tzIgWzGTwqA3onNvFyc',
        }

        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url: str, retry_times: int = 3) -> Optional[str]:
        """
        获取网页内容，有重试机制
        """
        for i in range(retry_times):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=10
                )
                response.raise_for_status()  # 检查响应状态
                return response.text
            except requests.RequestException as e:
                self.logger.error(f"第 {i + 1} 次请求失败: {url}")
                self.logger.error(f"错误信息: {str(e)}")
                if i == retry_times - 1:  # 最后一次重试
                    self.logger.error(f"达到最大重试次数，放弃请求: {url}")
                    return None
                time.sleep(2 ** i)  # 指数退避
        return None

    def process_csv(self, csv_path: str, output_path: str):
        """
        处理CSV文件中的URL
        """
        try:
            # 读取CSV文件
            df = pd.read_csv(csv_path)

            # 确保必要的列存在
            if 'url' not in df.columns or 'date' not in df.columns:
                raise ValueError("CSV必须包含'url'和'date'列")

            # 添加新列用于存储抓取结果
            df['content'] = None
            df['fetch_status'] = None
            df['fetch_time'] = None

            # 处理每个URL
            for index, row in df.iterrows():
                self.logger.info(f"处理第 {index + 1} 条记录: {row['url']}")

                content = self.fetch_page(row['url'])

                df.at[index, 'content'] = content
                df.at[index, 'fetch_status'] = 'success' if content else 'failed'
                df.at[index, 'fetch_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 每处理10条记录保存一次
                if (index + 1) % 10 == 0:
                    df.to_csv(output_path, index=False)
                    self.logger.info(f"保存进度: {index + 1} 条记录")

                # 添加随机延时，避免请求过于频繁
                time.sleep(1)

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
    test_url = "https://www.elobservador.com.uy/nota/lacalle-participo-de-entrega-de-campos-de-colonizacion-con-ausencias-de-senadores-blancos-2021112712182"
    content = scraper.fetch_page(test_url)
    if content:
        print("成功获取内容，内容长度:", len(content))
        print("内容前500个字符:")
        print(content)
    else:
        print("获取内容失败")

    # 如果要处理CSV文件，取消下面的注释
    # scraper.process_csv('input.csv', 'output.csv')


if __name__ == "__main__":
    main()