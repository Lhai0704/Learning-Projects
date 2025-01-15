from bs4 import BeautifulSoup
import csv

# 读取 HTML 文件
input_file = "searchResult.html"
output_file = "title_author_url.csv"

# 打开并解析 HTML 文件
with open(input_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# 查找所有的 li 标签
li_tags = soup.find_all('li', class_='x-base-grid__item')

# 创建 CSV 文件并写入标题和作者信息
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 写入 CSV 文件的表头
    writer.writerow(['Title', 'Author'])

    for li in li_tags:
        # 提取书名
        title_tag = li.find('h2', {'data-test': 'result-title', 'class': 'x-text1-lg'})
        # 提取作者名
        author_tag = li.find('h2', {'data-test': 'result-title', 'class': 'x-font-regular'})
        # 提取 URL
        url_tag = li.find('a', {'data-test': 'result-link'})

        # 如果找到标题、作者和 URL，则写入 CSV 文件
        if title_tag and author_tag and url_tag:
            title = title_tag.get_text(strip=True)
            author = author_tag.get_text(strip=True)
            url = url_tag['href']
            writer.writerow([title, author, url])

print(f"书籍信息已保存到 {output_file}")
