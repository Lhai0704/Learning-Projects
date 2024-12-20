# import csv
#
# # 从原始CSV中提取出 title 和 content 为 Error 的行，并保存到新的CSV中
# def extract_Error_rows(original_file, Error_file):
#     # 读取原始CSV文件
#     with open(original_file, mode='r', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         header = next(reader)  # 读取表头
#         rows = [row for row in reader]
#
#     # 提取出 title 和 content 为 Error 的行
#     Error_rows = [row for row in rows if row[2] == 'Error' and row[3] == 'Error']
#
#     # 将出错的行保存到新的CSV文件
#     with open(Error_file, mode='w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(header)  # 写入表头
#         writer.writerows(Error_rows)  # 写入出错的行
#
#     # 从原CSV中删除出错的行
#     rows = [row for row in rows if row[2] != 'Error' or row[3] != 'Error']
#
#     # 保存更新后的原CSV文件
#     with open(original_file, mode='w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(header)  # 写入表头
#         writer.writerows(rows)  # 写入非出错的行
#
#     print(f"出错的行已保存到 {Error_file}，并从原CSV文件中删除。")
#
# # 主程序，调用 extract_Error_rows
# def main():
#     original_file = 'data/filtered_china.csv'  # 替换为原始CSV文件路径
#     Error_file = 'china_Errors.csv'    # 新的CSV文件保存出错的行
#
#     extract_Error_rows(original_file, Error_file)
#
# if __name__ == '__main__':
#     main()



import csv

# 合并两个CSV文件，确保content列不会出现换行
def merge_csv(original_file, error_file, output_file):
    # 读取原始CSV文件
    with open(original_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 读取表头
        original_rows = [row for row in reader]

    # 读取error_rows.csv文件
    with open(error_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        error_rows = [row for row in reader]

    # 合并原始文件和错误行
    merged_rows = original_rows + error_rows

    # 保存合并后的内容到新CSV文件
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # 写入表头
        for row in merged_rows:
            # 确保content列中的文本没有换行
            row[3] = row[3].replace('\n', ' ').replace('\r', '')  # 将换行符替换为空格
            writer.writerow(row)

    print(f"CSV文件已合并并保存为 {output_file}")

# 主程序
def main():
    original_file = 'data/filtered_china.csv'  # 原始CSV文件路径
    error_file = 'china_Errors.csv'    # 错误行CSV文件路径
    output_file = 'merged_file.csv'  # 合并后的输出CSV文件路径

    merge_csv(original_file, error_file, output_file)

if __name__ == '__main__':
    main()
