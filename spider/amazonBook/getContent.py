import csv
import requests
from bs4 import BeautifulSoup

# 输入文件名和输出文件名
input_file = "title_url.csv"
output_file = "output.csv"

def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',  # Do Not Track
        'cookie': 'ubid-main=133-7360085-9255126; session-token=bBhuwaGjhv6OyHjj2zyJLyTXqrxvuWqRZYQxaI4GKPr4RDa0WYIx4Wy7KCg6EbTmy8GGPDqsQH+hnQ+eIs9QIJ1XC9mqhcY1EgZ2f3LsC2pKBNat+bPGg+lLhYGQAt3eEK4QAbMSoXnRmoXMVv+6mVxVrwJUzC7AYrByL9m65+cMgse6pnLOTrDBJmuapRUJLZv654NZIARaqLbifm4cpawT1CnERCGOzvlIQP+yq/g4V/VhnMScPGm5JO9nfktznTKVQaHpogxUJ8sSm1KpXsTBzTyAcXi0XkBNCyP+1NvPyx1oo4KN9dSJ6mfaiuQw40a00iqFkDY6i9JLTcjd7hcDiK8I6qcq; session-id=131-9774624-7298725; aws-session-id=765-4483862-7189953'
    }

    proxies = {
        'http': 'http://127.0.0.1:7890',  # Clash 默认 HTTP 代理端口
        'https': 'http://127.0.0.1:7890'  # Clash 默认 HTTPS 代理端口
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取author
        author_tag = soup.find('span', class_='author notFaded')
        author = author_tag.find('a', class_='a-link-normal').text.strip() if author_tag else None

        # 提取synopsis
        synopsis = None
        synopsis_container = soup.find('div', {
            'data-a-expander-name': 'book_description_expander',
            'class': 'a-expander-collapsed-height a-row a-expander-container a-spacing-base a-expander-partial-collapse-container'
        })
        if synopsis_container:
            synopsis_tag = synopsis_container.find('div',
                                                   class_='a-expander-content a-expander-partial-collapse-content')
            if synopsis_tag:
                spans = synopsis_tag.find_all('span')
                synopsis_parts = [span.get_text(strip=True) for span in spans]
                synopsis = " ".join(synopsis_parts)

        # 提取detailBullets中的键值对
        details = {}
        details_div = soup.find('div', id='detailBullets_feature_div')
        if details_div:
            items = details_div.find_all('li')
            for item in items:
                key_tag = item.find('span', class_='a-text-bold')
                value_tag = item.find_all('span')[-1]
                if key_tag and value_tag:
                    key = key_tag.text.strip().replace(':', '')
                    value = value_tag.text.strip()
                    details[key] = value

        return author, synopsis, details

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None, {}

def main():
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # 追加新列
    if 'author' not in fieldnames:
        fieldnames.append('author')
    if 'synopsis' not in fieldnames:
        fieldnames.append('synopsis')

    all_details_keys = set()

    # 爬取每个URL并更新数据
    for row in rows:
        url = row['url']
        print(f"Scraping {url}...")
        author, synopsis, details = scrape_page(url)
        row['author'] = author
        row['synopsis'] = synopsis

        # 收集所有的detail键
        for key, value in details.items():
            all_details_keys.add(key)
            row[key] = value

    # 确保所有新的键都在fieldnames中
    for key in all_details_keys:
        if key not in fieldnames:
            fieldnames.append(key)

    # 写回CSV文件
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
