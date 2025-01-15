import os
import csv
import xml.etree.ElementTree as ET


def extract_info_from_xml(folder_path, keywords):
    # 确保输出的文件夹存在
    output_folder = os.path.join(folder_path, "output")
    os.makedirs(output_folder, exist_ok=True)

    # 初始化用于存储数据的字典
    keyword_data = {keyword: [] for keyword in keywords}

    # 遍历文件夹中的所有XML文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xml'):
            file_path = os.path.join(folder_path, file_name)

            try:
                # 解析XML文件
                tree = ET.parse(file_path)
                root = tree.getroot()

                # 遍历所有的<url>标签
                for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                    loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    lastmod = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")

                    if loc is not None and lastmod is not None:
                        loc_text = loc.text
                        lastmod_text = lastmod.text.split('T')[0]  # 提取日期部分

                        # 检查loc是否包含任何关键词
                        for keyword in keywords:
                            if keyword in loc_text:
                                keyword_data[keyword].append([loc_text, lastmod_text])

            except ET.ParseError:
                print(f"Error parsing file: {file_path}")

    # 将结果写入CSV文件
    for keyword, rows in keyword_data.items():
        output_file = os.path.join(output_folder, f"{keyword}.csv")
        with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["url", "date"])
            writer.writerows(rows)

    print(f"Extraction completed. CSV files are saved in {output_folder}.")


# 使用示例
folder_path = "sitemaps"  # 替换为实际的文件夹路径
# keywords = ["china", "beijing", "chinas", "chino", "chinos", "hong-kong", "macao", "shanghai"]  # 替换为实际的关键词列表
keywords = ["pekin", "taiwan"]
extract_info_from_xml(folder_path, keywords)
