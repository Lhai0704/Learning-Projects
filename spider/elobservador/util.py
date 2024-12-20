# import csv
#
# # 定义文件路径
# input_file = 'china_data.csv'  # 输入的原始CSV文件
# output_file_1 = 'output_part1.csv'  # 保存第582行之前内容的新文件
# output_file_2 = 'output_part2.csv'  # 保存第582行及以后的内容的新文件
#
#
# # 分割CSV文件
# def split_csv(input_file, output_file_1, output_file_2, split_row):
#     try:
#         # 读取CSV文件
#         with open(input_file, 'r', newline='', encoding='utf-8') as infile:
#             reader = list(csv.reader(infile))
#
#             # 检查分割行号是否有效
#             if split_row < 1 or split_row > len(reader):
#                 raise ValueError(f"分割行号 {split_row} 超出范围，文件只有 {len(reader)} 行（包括表头）。")
#
#             header = reader[0]  # 获取表头
#             part1 = reader[:split_row]  # 第582行之前的内容
#             part2 = reader[split_row:]  # 第582行及以后的内容
#
#         # 写入第一个输出文件
#         with open(output_file_1, 'w', newline='', encoding='utf-8') as outfile1:
#             writer = csv.writer(outfile1)
#             writer.writerows(part1)
#
#         # 写入第二个输出文件
#         with open(output_file_2, 'w', newline='', encoding='utf-8') as outfile2:
#             writer = csv.writer(outfile2)
#             writer.writerow(header)  # 写入表头
#             writer.writerows(part2)
#
#         print(f"分割完成：\n  第1部分保存到 {output_file_1}\n  第2部分保存到 {output_file_2}")
#
#     except FileNotFoundError:
#         print(f"错误：文件 {input_file} 未找到！")
#     except Exception as e:
#         print(f"发生错误：{e}")
#
#
# # 调用函数
# split_csv(input_file, output_file_1, output_file_2, split_row=565)
# # -intrincada-negociacion-comercial-entre-eeuu-y-china-2019

#
# import pandas as pd
#
# # 读取第一个CSV文件
# df1 = pd.read_csv('china_data_part1.csv')
#
# # 读取第二个CSV文件
# df2 = pd.read_csv('china_data_part2.csv')
#
# # 拼接两个DataFrame，忽略索引，按行拼接
# result = pd.concat([df1, df2], ignore_index=True)
#
# # 将拼接后的结果保存到新的CSV文件
# result.to_csv('china_data.csv', index=False)




import os
import pandas as pd

def process_csv(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 删除指定列
    df = df.drop(columns=['fetch_status', 'fetch_time'], errors='ignore')

    # 确保列的顺序是：title, url, date, category, content
    required_columns = ['title', 'url', 'date', 'category', 'content']
    df = df[required_columns]

    # 处理category列，去掉空格和制表符
    df['category'] = df['category'].str.replace(r'\s+', '', regex=True)

    # 将处理后的数据直接保存回原文件
    df.to_csv(file_path, index=False)

def process_folder(folder_path):
    # 遍历文件夹中的所有CSV文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            process_csv(file_path)
            print(f"Processed file: {file_name}")

# 设定你要处理的文件夹路径
folder_path = 'data'  # 替换为你的文件夹路径
process_folder(folder_path)


# https://www.elobservador.com.uy/nota/-si-china-quiere-hacer-el-tlc-lo-vamos-a-hacer---canciller-rodolfo-nin-novoa-201723500


#
# import pandas as pd
#
# # 读取原始CSV文件
# input_file = 'data/china_data.csv'  # 替换为你的CSV文件路径
# df = pd.read_csv(input_file)
#
# # 筛选出包含"China"（大写）的行
# df_china = df[df['title'].str.contains('China', regex=False, na=False)]
#
# # 筛选出包含"china"（小写）的行
# df_china_lower = df[df['title'].str.contains('china', regex=False, na=False)]
#
# # 保存到新的CSV文件
# df_china.to_csv('data/elobservador_upper_china.csv', index=False)  # 保存包含"China"的行
# df_china_lower.to_csv('data/elobservador_lower_china.csv', index=False)  # 保存包含"china"的行
#
# print("CSV文件已分割并保存。")