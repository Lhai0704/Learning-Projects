import csv
import pandas as pd


def process_csv(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 删除第一列不含"China"的行
    df_filtered = df[df.iloc[:, 0].str.contains('chinos|Chinos', na=False)]

    # 去重
    df_unique = df_filtered.drop_duplicates()

    # 保存结果到新的CSV文件
    output_path = file_path.replace('.csv', '_processed_url.csv')
    df_unique.to_csv(output_path, index=False)

    print(f"原始行数: {len(df)}")
    print(f"删除不含China的行后行数: {len(df_filtered)}")
    print(f"去重后行数: {len(df_unique)}")
    print(f"处理后的文件已保存到: {output_path}")


# 使用示例
file_path = 'Cronica_chinos.csv'  # 请替换为您的CSV文件路径
process_csv(file_path)