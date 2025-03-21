from random import random

import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import random

def scrape_data(input_csv, output_csv):
    header = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ])
    }

    # 使用Session保持会话
    session = requests.Session()

    # 读取原始CSV文件
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        rows = list(reader)

    # 添加新字段到表头
    headers.extend(['date', 'content'])

    # 处理每一行URL并获取所需数据
    for row in rows:
        url = row[1]  # 第二列是URL
        try:
            response = session.get(url, headers=header, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 获取日期字段
            date_tag = soup.select_one('span.td-post-date time.entry-date')
            date = date_tag['datetime'] if date_tag else None

            # 格式化日期到 "YYYY-MM-DD"
            if date:
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

            # 获取正文内容
            content_div = soup.find('div', class_='td-post-content tagdiv-type')
            content = ''
            if content_div:
                paragraphs = content_div.find_all('p')
                content = '\n'.join(p.get_text(strip=True) for p in paragraphs)

            # 将新数据添加到行
            row.extend([date, content])

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            row.extend([None, None])  # 如果出错，填充空值

    # 写入新的CSV文件
    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        writer.writerows(rows)

# 示例调用
input_csv_file = 'Cronica_taiwan.csv'  # 输入的CSV文件
output_csv_file = 'Cronica_taiwan_content'  # 输出的CSV文件
scrape_data(input_csv_file, output_csv_file)
