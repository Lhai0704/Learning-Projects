import os
import time
import random
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


class SitemapDownloader:
    def __init__(self, base_url='https://rurales.elpais.com.uy', output_dir='rurales_sitemaps', min_delay=1, max_delay=3):
        """
        初始化下载器

        参数:
        - base_url: 网站基础URL
        - output_dir: 下载文件的保存目录
        - min_delay: 最小请求延迟(秒)
        - max_delay: 最大请求延迟(秒)
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.min_delay = min_delay
        self.max_delay = max_delay

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        #     'Accept': 'application/xml',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Connection': 'keep-alive',
        #     'Upgrade-Insecure-Requests': '1',
        #     'DNT': '1',  # Do Not Track
        # }

        cookies = {
            'cf_clearance': 'h4hv7nDh0_Oe5kgHpHWVIDbZ.mLedc6FYqUPfl2R6Q4-1734520735-1.2.1.1-_UCG.E8Qbc9xOr7FdOOy6XZwJKmTTti0hgd9NldKPa67SNNhr3wA8X.9K16eBwV9MxYTesGaxb3u6gdHAIT.RosMo836Vazyndo8_BuWoSKbalrL6NUBNiMjueVV7C0vE9FGNafULCj_0YazWfBD_giBhi45rDdM1Sc9fib48J8g1ZNjQMwIKZF6WTF69fXWXD0XDseq25N0jXH9..wUvduleZKuIgQmJcdggz00Qc4WP_CIQuUGrujMNu36RSg.ATW9i41nMbctmM3deOrhkJ5ftY5Hn66uNu_qUwMJ3AsyHuHDKdnPe4SBlezwO.HsiGDqR14aG1E54AbF5rBMHXmNIE.NGFhl5NKu3V9EO37kbn6Kl_D0dzBlR_BoY2geKCiSGEJyUkX8ZBFHXWY2QZqUGCU.Wj3p5KqUBDg7YM2pUGAVEn_r.jFWhRprEds8',
            # Cloudflare clearance cookie
        }

        # 创建会话
        self.session = requests.Session()

        # 设置通用请求头
        self.session.headers.update(self._get_headers())
        self.session.cookies.update(cookies)

    def _get_headers(self):
        """生成随机且复杂的请求头"""
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        ]

        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/xml',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',  # Do Not Track
        }

    def _random_delay(self):
        """随机延迟"""
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def _prepare_session(self):
        """
        准备会话，尝试获取必要的cookies
        """
        try:
            # 先访问主页获取初始cookies
            response = self.session.get(self.base_url)
            response.raise_for_status()
            print("成功获取初始会话")
        except requests.RequestException as e:
            print(f"获取初始会话失败: {e}")

    def download_sitemaps(self, sitemap_index_url):
        """
        下载sitemap索引中的所有子sitemap

        参数:
        - sitemap_index_url: sitemap索引文件的URL
        """
        # 准备会话
        self._prepare_session()

        try:
            # 下载sitemap索引文件
            response = self.session.get(sitemap_index_url)
            response.raise_for_status()

            self._random_delay()

            # 解析XML
            root = ET.fromstring(response.text)

            # 命名空间处理
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # 查找所有sitemap位置
            sitemap_locations = root.findall('.//ns:loc', namespace)

            # 存储下载成功和失败的URL
            downloaded_sitemaps = []
            failed_sitemaps = []

            # 下载每个子sitemap
            for loc_elem in sitemap_locations:
                sitemap_url = loc_elem.text

                try:
                    # 获取文件名
                    parsed_url = urlparse(sitemap_url)
                    filename = os.path.basename(parsed_url.path)

                    # 更新请求头
                    self.session.headers.update(self._get_headers())

                    # 下载文件
                    sitemap_response = self.session.get(sitemap_url)
                    sitemap_response.raise_for_status()

                    # 保存文件
                    file_path = os.path.join(self.output_dir, filename)
                    with open(file_path, 'wb') as f:
                        f.write(sitemap_response.content)

                    downloaded_sitemaps.append(sitemap_url)
                    print(f"成功下载: {sitemap_url}")

                    self._random_delay()

                except requests.RequestException as e:
                    failed_sitemaps.append(sitemap_url)
                    print(f"下载失败: {sitemap_url}, 错误: {e}")

            # 打印下载结果摘要
            print("\n下载摘要:")
            print(f"总sitemap数: {len(sitemap_locations)}")
            print(f"成功下载: {len(downloaded_sitemaps)}")
            print(f"下载失败: {len(failed_sitemaps)}")

            if failed_sitemaps:
                print("\n失败的sitemap:")
                for url in failed_sitemaps:
                    print(url)

            return downloaded_sitemaps, failed_sitemaps

        except requests.RequestException as e:
            print(f"无法获取sitemap索引: {e}")
            return [], []


# 使用示例
if __name__ == '__main__':
    sitemap_index_url = 'https://rurales.elpais.com.uy/sitemap.xml'
    downloader = SitemapDownloader()
    downloader.download_sitemaps(sitemap_index_url)