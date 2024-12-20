import requests
from bs4 import BeautifulSoup


def crawl_china_news(url):
    # 发送HTTP请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    print(response)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)
    # 找到所有class为"entry-title td-module-title"的div
    news_items = soup.find_all('h3', class_='entry-title td-module-title')

    print(news_items)
    # 存储新闻信息的列表
    news_list = []

    # 遍历并提取标题和链接
    for item in news_items:
        link = item.find('a')
        if link:
            news_list.append({
                'title': link.text.strip(),
                'url': link['href']
            })

    return news_list


# 示例使用
url = 'https://www.cronicas.com.uy/page/1/?s=China'
news = crawl_china_news(url)

# 打印结果
for item in news:
    print(f"标题: {item['title']}")
    print(f"链接: {item['url']}")
    print('---')