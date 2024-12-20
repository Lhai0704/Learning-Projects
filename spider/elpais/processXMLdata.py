import pandas as pd

def filter_and_deduplicate(csv_file, keyword, output_file):
    # 读取CSV文件
    df = pd.read_csv(csv_file)

    # 根据关键字过滤URL列
    filtered_df = df[df['url'].str.contains(keyword, na=False)]

    # 去重：移除重复的行
    deduplicated_df = filtered_df.drop_duplicates()

    # 保存到新的CSV文件
    deduplicated_df.to_csv(output_file, index=False)
    print(f"处理完成，结果已保存到 {output_file}")

# 使用示例
csv_file = 'XML_data.csv'  # 输入文件路径
keyword = 'beijing'  # 你要查找的关键字
output_file = 'filtered_beijing.csv'  # 输出文件路径

filter_and_deduplicate(csv_file, keyword, output_file)
