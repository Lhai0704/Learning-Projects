# Sitemap: https://www.elobservador.com.uy/sitemap/images-full/sitemap-index.xml        应该是图片的url，不用管
# Sitemap: https://www.elobservador.com.uy/sitemap/news-full/sitemap-index.xml        这里面应该是全部的，下载里面的gz文件，解压得到xml
# Sitemap: https://www.elobservador.com.uy/sitemap.xml               好像都是最近一两天的
# Sitemap: https://www.elobservador.com.uy/sitemap-news.xml         也是最近一两天的


import requests
import os
import gzip
import shutil
import xml.etree.ElementTree as ET

# 配置 headers 和 cookies
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/xml',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track
}
COOKIES = {
    'cf_clearance': 'awGpleLyglDmDCr4fggF6bRzC.6oGvPvq4vTmAnuVTk-1734654548-1.2.1.1-3Cve7vhWguADJeYFM9PHT0SsraPVnYKq2bpT_hIOfturo_NUECBthcBHgaNoCFYhmzMIfJI673hH3hu8l3Pk3Pd0yzogTFo0c9XAM5gYbxhQJinP_6NH3WsL_RWt2DRfjeCi0yvfMWMWODaDiylBFyTpAEtQNn2f4_5Uru4B8cnScX8QGkZkMkS7DG0zOO1EeysZVCY982s8GSfNHMZ1UI4E0ApGr.2bJxPO2u9w0nu1bPDbvFH1nYlPTWa0HBv0nd9ZKwEbFx5RSzvASmF42RjeZPSmd3Za9bPUaWwL80cfte_76T_Jp5S6R6eMsMjluiSp_vkI8_bG2_WaMlGbeECJ.Bnr2ycyb1lE1VIHOAPQLk0vXl5CLSJTjMdH5iHyEat43DABYVEdExUJr80QOFP2J1CTvhN6G1in8fz4iDnWjeHIU4k6FaJY6lgODQKv',
}

# 定义 sitemap 的 URL
SITEMAP_URL = "https://www.elobservador.com.uy/sitemap/news-full/sitemap-index.xml"

# 创建一个目录用于存放下载的 .gz 文件和解压后的文件
DOWNLOAD_DIR = "sitemaps"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 下载并解析 sitemap
response = requests.get(SITEMAP_URL, headers=HEADERS, cookies=COOKIES)
response.raise_for_status()

# 解析 XML
root = ET.fromstring(response.content)

# Sitemap 的命名空间
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# 遍历所有的 <loc> 标签，下载 .gz 文件
for sitemap in root.findall('ns:sitemap', namespace):
    loc = sitemap.find('ns:loc', namespace).text
    if loc.endswith('.gz'):
        print(f"Downloading: {loc}")
        gz_response = requests.get(loc, headers=HEADERS, cookies=COOKIES, stream=True)
        gz_response.raise_for_status()

        # 保存 .gz 文件
        gz_filename = os.path.join(DOWNLOAD_DIR, os.path.basename(loc))
        with open(gz_filename, 'wb') as gz_file:
            shutil.copyfileobj(gz_response.raw, gz_file)
        print(f"Saved: {gz_filename}")

        # 解压 .gz 文件
        extracted_filename = gz_filename.replace('.gz', '')
        with gzip.open(gz_filename, 'rb') as f_in:
            with open(extracted_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Extracted: {extracted_filename}")

print("All .gz files downloaded and extracted.")
