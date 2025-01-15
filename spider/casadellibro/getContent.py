import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_and_update_csv(input_csv, output_csv):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',  # Do Not Track
    }

    proxies = {
        'http': 'http://127.0.0.1:7890',  # Clash 默认 HTTP 代理端口
        'https': 'http://127.0.0.1:7890'  # Clash 默认 HTTPS 代理端口
    }

    # 读取CSV文件
    df = pd.read_csv(input_csv)

    # 初始化动态列集合
    dynamic_columns = set()

    for index, row in df.iterrows():
        url = row['Url']  # 假设第三列的列名为'url'
        try:
            # 请求网页内容
            response = requests.get(url, headers=headers, proxies=proxies,)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # 提取分类信息
            categories = soup.find_all("a", class_="brand")
            category_list = [category.text.strip() for category in categories]
            df.at[index, 'category'] = "/".join(category_list)

            # 提取概要信息
            synopsis = soup.find("h2", class_="f-w-6 s-7-text balance-title resumen mt-2 svelte-ud4r8d")
            df.at[index, 'synopsis'] = synopsis.text.strip() if synopsis else ""

            # 提取详细描述信息
            detailed_description = soup.find("div", class_="resumen-content")
            df.at[index, 'detailed_description'] = detailed_description.text.strip() if detailed_description else ""

            # 提取动态键值对数据
            characteristics = soup.find_all(["div", "h3"], class_="campo")
            for char in characteristics:
                key_tag = char.find("b")
                value_tag = char.find("span")
                if key_tag and value_tag:
                    key = key_tag.text.strip().replace(":", "")
                    value = value_tag.text.strip()
                    dynamic_columns.add(key)
                    df.at[index, key] = value

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue

    # 确保所有动态列出现在最终的CSV中
    for column in dynamic_columns:
        if column not in df.columns:
            df[column] = ""

    # 保存更新后的CSV
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')


# 使用示例
input_csv = "title_author_url.csv"  # 输入CSV文件路径
# input_csv = "test.csv"
output_csv = "output.csv"  # 输出CSV文件路径
scrape_and_update_csv(input_csv, output_csv)
