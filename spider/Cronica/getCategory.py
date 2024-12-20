import pandas as pd

# 读取CSV文件
file_path = "Cronica_data/Cronica_Upper_China_data.csv"  # 替换为你的文件路径
df = pd.read_csv(file_path)

# 定义一个函数从URL中提取特定部分
def extract_section(url):
    try:
        return url.split("/")[3]  # 根据URL的结构，提取第三个斜杠后的部分
    except IndexError:
        return None

# 应用函数，提取新列
df['category'] = df['url'].apply(extract_section)

# 调整列的位置，将新列插入到第二列和第三列之间
cols = df.columns.tolist()
cols.insert(3, cols.pop(-1))  # 将最后一列移到第三列的位置
df = df[cols]

# 保存为新的CSV文件
output_file = "Cronica_data/Cronica_upper_China.csv"  # 替换为你的输出文件路径
df.to_csv(output_file, index=False)

print(f"新文件已保存为 {output_file}")
