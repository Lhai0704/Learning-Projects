import csv


def find_rows_without_china(file_path):
    # 用于存储不含"China"的行
    rows_without_china = []

    # 打开CSV文件
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # 创建CSV读取器
        csv_reader = csv.reader(csvfile)

        # 跳过第一行标题
        next(csv_reader)

        # 遍历每一行
        for row_index, row in enumerate(csv_reader, start=2):  # 从第2行开始计数
            # 检查第一列是否不包含"China"
            if ("China" not in row[0]) and ("china" not in row[0]):
                rows_without_china.append(row)

    return rows_without_china


# 使用示例
file_path = 'Cronica_China.csv'  # 请替换为您的CSV文件路径
result = find_rows_without_china(file_path)

print(f"找到 {len(result)} 行不包含 'China':")
for row in result:
    print(row)