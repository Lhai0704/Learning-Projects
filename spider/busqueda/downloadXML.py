
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
    'cf_clearance': 'tF0MAEnp6bTpT9Pb6aS3kgp.hDj2sOFlRmuhi6n4z6o-1734669258-1.2.1.1-CJwK2U7OFnTfWAR2W0nArcFAlLp2daQZ_e03Ds0X0edvQ.KMy_66z6USzYgtaqm8woHaM.iYtES3hdyzN.gbA4CwJol46l8cvRVNcmKSFtqw11TAfhHqjM3j6yxgU8xRQA82EtRQrGnY8bXuzw_Wuq9wh9Xqa8hukgYFnOIxLHdDPyoYcUA5iNxDZ0i7SpEoM3IcISw7Aw7fWMBKz1uEvFeEZXJjLigm_GBdn2T13ZxDhFU.Z9Q3PyrEOrNz8dEeQ8NMNpBv0qk.WMECFrvSsJ48jhEi3RZavDtvSRTvaC634WmRZbxmUra.5pQiP3Nw20qjwVx._jvLVUJsLqn3H6BOZR0UcvGdOucNC_AZRViqNe6pLf9RX.8KD4hAbDsIaGFOtbVB1dAcbPOKslu6tvVa.o9Gy9lIs1AmftZEdhfDzL.tMq.KPGFwX37XkIK1',
}

# 定义 sitemap 的 URL
SITEMAP_URL = "https://www.busqueda.com.uy/sitemap/news-full/sitemap-index.xml"

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
