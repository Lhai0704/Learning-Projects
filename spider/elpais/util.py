# 替换
# import pandas as pd
#
# # 1. 读取CSV文件
# file_path = 'data/elpais_data/elpais_china.csv'  # 请替换为你的CSV文件路径
# df = pd.read_csv(file_path)
#
# # 2. 查找url列中包含"xxx"的行并修改category列
# df.loc[df['url'].str.contains('https://rurales.elpais.com.uy/brasil-china-y-el-gran-signo-de-interrogacion-en-el-mundo-de-la-carne', na=False), 'category'] = ''
#
# # 3. 直接覆盖原文件
# df.to_csv(file_path, index=False)
#
# print("原CSV文件已修改并保存。")




# 删除行末两个逗号
# import csv
#
# # 输入和输出文件路径
# input_file = 'data/filtered_chino.csv'
# output_file = 'output.csv'
#
# # 打开原始 CSV 文件和目标 CSV 文件
# with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='',
#                                                                          encoding='utf-8') as outfile:
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)
#
#     for row in reader:
#         # 如果行末有两个空值（即两个逗号），则移除它们
#         if len(row) > 4 and row[-2:] == ['', '']:
#             row = row[:-2]
#         writer.writerow(row)
#
# print(f"处理完成，清理后的文件保存在：{output_file}")


# 去除换行
# import pandas as pd
#
# # 读取CSV文件
# df = pd.read_csv('data/elpais_data/elpais_hongkong.csv', encoding='utf-8')
#
# # 去除所有字段中的换行符
# df = df.applymap(lambda x: x.replace('\n', ' ') if isinstance(x, str) else x)
#
# # 将修改后的DataFrame保存为新的CSV文件
# df.to_csv('output.csv', index=False, encoding='utf-8')


import pandas as pd

# 读取原始CSV文件
input_file = 'data/elpais_data/elpais_china.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(input_file)

# 筛选出包含"China"（大写）的行
df_china = df[df['title'].str.contains('China', regex=False, na=False)]

# 筛选出包含"china"（小写）的行
df_china_lower = df[df['title'].str.contains('china', regex=False, na=False)]

# 保存到新的CSV文件
df_china.to_csv('data/elpais_data/elpais_upper_china.csv', index=False)  # 保存包含"China"的行
df_china_lower.to_csv('data/elpais_data/elpais_lower_china.csv', index=False)  # 保存包含"china"的行

print("CSV文件已分割并保存。")



