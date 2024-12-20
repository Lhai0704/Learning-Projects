import os
import xml.etree.ElementTree as ET
from pathlib import Path


def convert_urls_to_lowercase(xml_file_path):
    """
    将 XML 文件中 loc 标签内的 URL 转换为小写

    Args:
        xml_file_path: XML 文件的路径
    """
    try:
        # 解析 XML 文件
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # 定义命名空间
        namespaces = {
            'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
        }

        # 查找所有的 loc 元素并转换 URL
        modified = False
        for loc in root.findall('.//ns:loc', namespaces):
            original_url = loc.text
            lowercase_url = original_url.lower()
            if original_url != lowercase_url:
                loc.text = lowercase_url
                modified = True

        # 如果有修改，保存文件
        if modified:
            # 保持原始的 XML 声明
            declaration = '<?xml version="1.0" encoding="UTF-8"?>'
            xml_content = ET.tostring(root, encoding='unicode', xml_declaration=False)

            with open(xml_file_path, 'w', encoding='utf-8') as f:
                f.write(declaration + '\n' + xml_content)

        return modified

    except Exception as e:
        print(f"处理文件 {xml_file_path} 时发生错误: {str(e)}")
        return False


def process_xml_directory(directory_path):
    """
    处理指定目录下的所有 XML 文件

    Args:
        directory_path: 包含 XML 文件的目录路径
    """
    directory = Path(directory_path)
    processed_count = 0
    modified_count = 0

    for xml_file in directory.glob('*.xml'):
        processed_count += 1
        if convert_urls_to_lowercase(xml_file):
            modified_count += 1
            print(f"已处理并修改文件: {xml_file}")
        else:
            print(f"已处理文件 (无需修改): {xml_file}")

    print(f"\n处理完成！")
    print(f"总共处理的文件数: {processed_count}")
    print(f"修改的文件数: {modified_count}")


# 使用示例
if __name__ == "__main__":
    # 替换为你的 XML 文件所在的目录路径
    xml_directory = "sitemaps"
    process_xml_directory(xml_directory)