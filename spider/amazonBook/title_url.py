import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
import random


def scrape_amazon_page(url, base_url='https://www.amazon.com'):
    """抓取单个页面的数据"""

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
        # 添加随机延迟，避免被反爬
        time.sleep(random.uniform(2, 4))

        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        books_data = []

        # 找到所有书籍div
        book_divs = soup.find_all('div', {'data-cy': 'title-recipe'})

        for div in book_divs:
            try:
                # 提取 title
                title_element = div.find('h2', class_='a-size-base-plus a-spacing-none a-color-base a-text-normal')
                title = title_element.get_text(strip=True) if title_element else ""

                # 提取 author
                # author_element = div.find('span', class_='a-size-base', text=True)
                # author = author_element.get_text(strip=True) if author_element else ""

                # 提取 URL
                link_element = div.find('a', class_='a-link-normal')
                full_url = f"https://www.amazon.com{link_element['href']}" if link_element else ""

                books_data.append({
                    'title': title,
                    'url': full_url
                })

            except Exception as e:
                print(f"Error processing book entry: {str(e)}")
                continue

        return books_data

    except requests.RequestException as e:
        print(f"Error fetching page {url}: {str(e)}")
        return []


def main():
    base_url = "https://www.amazon.com/s?k=medicina+china&i=stripbooks&rh=n%3A283155%2Cp_n_feature_twenty-five_browse-bin%3A3291439011&dc&language=es_US&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=31IV6A4GJ0OGL&qid=1736849847&rnid=3291435011&sprefix=%2Caps%2C393&xpid=Th9chnVYxCTr0"
    total_pages = 13

    # 创建CSV文件
    with open('title_url.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 遍历所有页面
        for page in range(1, total_pages + 1):
            print(f"Scraping page {page} of {total_pages}")

            # 构建页面URL
            page_url = f"{base_url}&page={page}" if page > 1 else base_url

            # 抓取当前页面数据
            books_data = scrape_amazon_page(page_url)

            # 写入CSV
            for book in books_data:
                writer.writerow(book)

            print(f"Completed page {page}")


if __name__ == "__main__":
    main()