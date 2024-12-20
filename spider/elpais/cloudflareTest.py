import requests

# 目标URL
url = "https://www.elpais.com.uy/sitemap.xml"

# 自定义的User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/xml',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track
}

# 模拟的cookie（假设你从浏览器的开发者工具中获得的cookies）
cookies = {
    'cf_clearance': 'h4hv7nDh0_Oe5kgHpHWVIDbZ.mLedc6FYqUPfl2R6Q4-1734520735-1.2.1.1-_UCG.E8Qbc9xOr7FdOOy6XZwJKmTTti0hgd9NldKPa67SNNhr3wA8X.9K16eBwV9MxYTesGaxb3u6gdHAIT.RosMo836Vazyndo8_BuWoSKbalrL6NUBNiMjueVV7C0vE9FGNafULCj_0YazWfBD_giBhi45rDdM1Sc9fib48J8g1ZNjQMwIKZF6WTF69fXWXD0XDseq25N0jXH9..wUvduleZKuIgQmJcdggz00Qc4WP_CIQuUGrujMNu36RSg.ATW9i41nMbctmM3deOrhkJ5ftY5Hn66uNu_qUwMJ3AsyHuHDKdnPe4SBlezwO.HsiGDqR14aG1E54AbF5rBMHXmNIE.NGFhl5NKu3V9EO37kbn6Kl_D0dzBlR_BoY2geKCiSGEJyUkX8ZBFHXWY2QZqUGCU.Wj3p5KqUBDg7YM2pUGAVEn_r.jFWhRprEds8',  # Cloudflare clearance cookie
}

# 创建会话
session = requests.Session()

# 为会话设置自定义header和cookies
session.headers.update(headers)
session.cookies.update(cookies)

# 发送请求
response = session.get(url)

# 处理响应
if response.status_code == 200:
    sitemap_content = response.text
    print(sitemap_content)  # 输出XML内容
else:
    print(f"Failed to retrieve sitemap: {response.status_code}")
