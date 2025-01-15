import csv

# 提取content列为空的行，并保存到新的CSV文件中
def extract_empty_content_rows(original_file, empty_content_file):
    # 读取原始CSV文件
    with open(original_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 读取表头
        rows = [row for row in reader]

    # 提取出content列为空的行
    empty_content_rows = [row for row in rows if not row[3].strip()]  # content列为空或者是空白

    # 将提取出来的空content行保存到新的CSV文件
    with open(empty_content_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # 写入表头
        writer.writerows(empty_content_rows)  # 写入content列为空的行

    # 从原CSV中删除这些content列为空的行
    rows = [row for row in rows if row[3].strip()]  # 只保留content列不为空的行

    # 保存更新后的原CSV文件
    with open(original_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # 写入表头
        writer.writerows(rows)  # 写入更新后的行

    print(f"content列为空的行已保存到 {empty_content_file}，并从原CSV文件中删除。")

# 主程序
def main():
    original_file = 'filtered_taiwan.csv'  # 原始CSV文件路径
    empty_content_file = 'empty_content_rows_taiwan.csv'  # 保存content列为空的行的CSV文件路径

    extract_empty_content_rows(original_file, empty_content_file)

if __name__ == '__main__':
    main()
