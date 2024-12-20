import os
import xml.etree.ElementTree as ET
import csv


def extract_xml_data(xml_file):
    """从XML文件中提取loc和lastmod标签内容"""
    url_data = []

    # 解析XML文件
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 获取命名空间
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # 查找所有url标签
        for url in root.findall(".//ns:url", namespaces):
            loc = url.find("ns:loc", namespaces).text if url.find("ns:loc", namespaces) is not None else ""
            lastmod = url.find("ns:lastmod", namespaces).text if url.find("ns:lastmod", namespaces) is not None else ""

            # 将loc和lastmod内容保存到列表
            url_data.append([loc, lastmod])
    except ET.ParseError as e:
        print(f"解析文件 {xml_file} 时出错: {e}")
    return url_data


def process_folders(input_folders, output_csv):
    """处理多个文件夹中的所有XML文件并将结果保存到CSV文件"""
    all_url_data = []

    # 遍历每个文件夹中的所有XML文件
    for folder in input_folders:
        if not os.path.isdir(folder):
            print(f"{folder} 不是一个有效的文件夹路径!")
            continue

        for filename in os.listdir(folder):
            if filename.endswith(".xml"):
                file_path = os.path.join(folder, filename)
                print(f"处理文件: {file_path}")

                # 提取当前XML文件中的数据
                url_data = extract_xml_data(file_path)
                all_url_data.extend(url_data)  # 将数据合并到总列表中

    # 将提取的数据写入CSV文件
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["url", "time"])  # 写入表头
        writer.writerows(all_url_data)  # 写入数据

    print(f"所有数据已保存到 {output_csv}")


# 使用示例
input_folders = ["sitemaps", "rurales_sitemaps"]  # 输入文件夹路径列表
output_csv = "XML_data.csv"  # 输出CSV文件路径

process_folders(input_folders, output_csv)
