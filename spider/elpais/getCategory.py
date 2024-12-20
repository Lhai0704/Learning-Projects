import os
import csv
from collections import Counter
import urllib.parse


def extract_category(url):
    """
    提取URL中的类别信息，并返回父类别/子类别（如果有）
    假设URL格式是 https://www.elpais.com.uy/{category}/{subcategory}/{...}
    """
    # 解析URL路径部分
    path = urllib.parse.urlparse(url).path
    parts = path.strip('/').split('/')

    # 如果路径中有多个部分，组合父类别和子类别
    if len(parts) > 1:
        category = parts[-2]  # 父类别
        subcategory = parts[-1]  # 子类别
        return f'{category}/{subcategory}'  # 组合成 "父类别/子类别" 的格式
    else:
        return None


def process_csv_files(folder_path):
    """
    遍历文件夹中的所有CSV文件，提取URL中的类别并统计
    """
    category_counter = Counter()  # 用于统计类别的出现频率

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # 打开并读取CSV文件
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)

                # 跳过标题行（如果有的话）
                next(reader, None)

                # 读取每行并提取URL的类别
                for row in reader:
                    if row:  # 确保行不为空
                        url = row[0]  # 假设URL在每行的第一列
                        category = extract_category(url)
                        if category:
                            category_counter[category] += 1

    return category_counter


def main():
    folder_path = 'data'  # 设置你的CSV文件夹路径
    category_counter = process_csv_files(folder_path)

    # 打印统计结果
    for category, count in category_counter.items():
        print(f'{category}: {count}')


if __name__ == '__main__':
    main()
