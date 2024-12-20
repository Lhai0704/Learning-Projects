import requests
from bs4 import BeautifulSoup
import csv
import time

# 定义请求头和cookie（需要根据目标网站调整）
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/xml',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track
}

cookies = {
    # 'cookie_name': 'cookie_value'  # 根据实际情况填入cookie
    'cf_clearance': 'r310ymE0OHePzdPDfasuNpSlWwLt6_sD2Q.Sa1C0AUo-1734566367-1.2.1.1-nILkbCmkbpv6NOtZsEdZZuAL.TxXSylbWR3hkAInGL18uJDyaH3le39bXcwOiqJeHYFHI4t53yqBgZw3ZJnisWFYGwneFAoQoIo5s2cqZrMGJp89Sjp4SovJk3Yo.MHl6GtdBuIffzn4UR7JM8PmYD6qEAXh2iHvopjPJavBACtDVYRl5mj8w.9qxft5wLFOSY2n.E96DY6Zm3UrOvpTLuJ55x98KWfJiHQ534uc61mslW9AAnizhF555yZQKKxm8h4l3z0D4BhntKjgS09npUJcy6L8rcWtze10muofcfpFKMb28h0ts83PAYqY9k76DTUCmLc68SNbPYs96TIRKTJkvJ6VP3QKK2wdtYY1WvsGnWFDUFl5FYdc6rBfI3Y4__5fLYRgCLJAH6BaHg_qRPpoGd6sk4BmfVb4GG7Q3A5.oZjPs8pw0CONjlbptOrK',
}


# 读取CSV文件，并提取URL与时间
def read_csv(file_name):
    with open(file_name, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头
        rows = [row for row in reader]
    return header, rows


# 获取网页内容并提取数据
def get_page_data(url):
    try:
        # 发起请求
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取标题（<h1 class="Page-headline">）
        title_tag = soup.find('h1', class_='Page-headline')
        title = title_tag.text.strip() if title_tag else 'No Title'

        # 获取内容（<div class="RichTextArticleBody RichTextBody"> 内的 <p> 标签的文本，忽略其中的 <div> 标签）
        content_div = soup.find('div', class_='RichTextArticleBody RichTextBody')
        content = ''
        if content_div:
            p_tags = content_div.find_all('p')  # 获取所有<p>标签
            for p in p_tags:
                # 忽略<p>标签内部的<div>标签
                for div in p.find_all('div'):
                    div.decompose()  # 删除<div>标签

                # 拼接<p>标签内的文本，顺序保留
                text_parts = []
                for element in p.children:
                    if isinstance(element, str):  # 纯文本
                        text_parts.append(element.strip())
                    elif element.name == 'b':  # <b>标签中的文本
                        text_parts.append(element.get_text(strip=True))
                    elif element.name == 'a':  # <a>标签中的文本
                        text_parts.append(element.get_text(strip=True))

                content += ' '.join(text_parts) + ' '  # 将所有部分拼接成一个字符串

        return title, content.strip()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return 'Error', 'Error'


# 更新CSV文件
def update_csv(file_name, header, rows, updated_data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # 写入表头
        for i, row in enumerate(rows):
            row.append(updated_data[i][0])  # 添加title
            row.append(updated_data[i][1])  # 添加content
            writer.writerow(row)

# 主程序
def main():
    file_name = 'china_Errors.csv'  # 替换为你的CSV文件名
    header, rows = read_csv(file_name)

    updated_data = []  # 用于存储更新后的数据
    for row in rows:
        url = row[0]  # 第一列为URL
        print(f"Processing {url}...")
        title, content = get_page_data(url)
        updated_data.append((title, content))
        time.sleep(1)  # 防止请求过快被封禁，适当的延时

    # 更新原CSV文件
    update_csv(file_name, header + ['title', 'content'], rows, updated_data)
    print("CSV file updated successfully.")


if __name__ == '__main__':
    main()