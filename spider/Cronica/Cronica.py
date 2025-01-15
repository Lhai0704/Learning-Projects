# 给定关键词和页数，输出csv文件，第一列为title，第二列为url

import requests
from bs4 import BeautifulSoup
import csv
import random
import time

# 定义爬取函数
def crawl_china_news(page):
    url = f'https://www.cronicas.com.uy/page/{page}/?s=taiwan'
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ])
    }

    # 使用Session保持会话
    session = requests.Session()

    retries = 3  # 最大重试次数
    response = None
    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break  # 如果成功，则跳出重试循环
        except requests.RequestException as e:
            print(f"Error fetching page {page}, attempt {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(random.uniform(2, 5))  # 随机等待后重试
            else:
                return []  # 如果失败次数达到最大值，则返回空列表

    if response is None:
        return []

    # 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all('h3', class_='entry-title td-module-title')

    news_list = []
    for item in news_items:
        link = item.find('a')
        if link:
            news_list.append({
                'title': link.text.strip(),
                'url': link['href']
            })

    return news_list

# 保存到CSV的函数
def save_to_csv(data, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'url'])
        if file.tell() == 0:
            writer.writeheader()  # 如果文件为空，写入表头
        writer.writerows(data)

# 主函数
if __name__ == "__main__":
    filename = 'Cronica_taiwan.csv'

    for page in range(1, 5):  # 循环爬取
        print(f"Crawling page {page}...")
        news = crawl_china_news(page)
        save_to_csv(news, filename)
        print(f"Page {page} fetched {len(news)} items and saved to {filename}.")

        # 随机延时以模拟人类行为
        time.sleep(random.uniform(1, 3))
