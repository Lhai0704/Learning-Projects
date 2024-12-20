# import os
# import pandas as pd
#
# def process_csv(file_path):
#     # 读取CSV文件
#     df = pd.read_csv(file_path)
#
#     # 删除指定列
#     df = df.drop(columns=['fetch_status', 'fetch_time'], errors='ignore')
#
#     # 确保列的顺序是：title, url, date, category, content
#     required_columns = ['title', 'url', 'date', 'category', 'content']
#     df = df[required_columns]
#
#     # 处理category列，去掉空格和制表符
#     # df['category'] = df['category'].str.replace(r'\s+', '', regex=True)
#
#     # 将处理后的数据直接保存回原文件
#     df.to_csv(file_path, index=False)
#
# def process_folder(folder_path):
#     # 遍历文件夹中的所有CSV文件
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith('.csv'):
#             file_path = os.path.join(folder_path, file_name)
#             process_csv(file_path)
#             print(f"Processed file: {file_name}")
#
# # 设定你要处理的文件夹路径
# folder_path = 'data'  # 替换为你的文件夹路径
# process_folder(folder_path)



import pandas as pd

# 读取原始CSV文件
input_file = 'data/china_data.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(input_file)

# 筛选出包含"China"（大写）的行
df_china = df[df['title'].str.contains('China', regex=False, na=False)]

# 筛选出包含"china"（小写）的行
df_china_lower = df[df['title'].str.contains('china', regex=False, na=False)]

# 保存到新的CSV文件
df_china.to_csv('data/busqueda_upper_china.csv', index=False)  # 保存包含"China"的行
df_china_lower.to_csv('data/busqueda_lower_china.csv', index=False)  # 保存包含"china"的行

print("CSV文件已分割并保存。")