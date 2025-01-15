import pandas as pd
import re
import csv


def inspect_problematic_lines(file_path, start_line, num_lines=10):
    """检查问题行及其周围的行"""
    start_idx = max(1, start_line - 5)  # 从问题行前5行开始
    end_idx = start_line + 5  # 到问题行后5行结束

    print(f"\n检查第 {start_idx} 到 {end_idx} 行的内容:")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if start_idx <= i <= end_idx:
                    print(f"行 {i}: {line.strip()}")
                if i > end_idx:
                    break
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")


def extract_category(url):
    pattern = r'\.com\.uy\/(.+?)(?:/[^/]+)?$'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def process_csv(input_file, output_file):
    # 首先检查文件内容
    print("正在检查CSV文件结构...")
    problematic_lines = []

    # 使用csv模块先检查文件
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头
        for i, row in enumerate(reader, 2):  # 从第2行开始计数
            if len(row) != 4:  # 期望4个字段
                problematic_lines.append((i, len(row), row))
                if len(problematic_lines) <= 3:  # 只显示前3个问题
                    print(f"\n问题行 {i}:")
                    print(f"预期4个字段，实际发现{len(row)}个字段")
                    print("字段内容:", row)

    if problematic_lines:
        print(f"\n发现 {len(problematic_lines)} 个问题行")
        # 检查第一个问题行周围的内容
        if problematic_lines:
            first_problem_line = problematic_lines[0][0]
            inspect_problematic_lines(input_file, first_problem_line)

        print("\n建议解决方案：")
        print("1. 使用更严格的CSV读取参数")
        print("2. 手动检查并修复问题行")

        # 尝试使用更严格的参数读取
        try:
            df = pd.read_csv(input_file,
                             quoting=csv.QUOTE_ALL,  # 所有字段都用引号
                             escapechar='\\',
                             on_bad_lines='skip')  # 跳过问题行

            # 从URL提取类别
            df['category'] = df['url'].apply(extract_category)

            # 重命名time列为date
            df = df.rename(columns={'time': 'date'})

            # 重新排列列的顺序
            df = df[['title', 'url', 'date', 'category', 'content']]

            # 保存到新的CSV文件
            df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

            print(f"\n处理完成:")
            print(f"- 总行数: {len(df)}")
            print(f"- 跳过的问题行数: {len(problematic_lines)}")
            print(f"- 成功提取的类别数: {df['category'].notna().sum()}")

            return df

        except Exception as e:
            print(f"\n使用严格参数读取仍然失败: {str(e)}")
            raise
    else:
        print("文件检查完成，未发现格式问题。")
        return process_csv_normal(input_file, output_file)


def process_csv_normal(input_file, output_file):
    """处理格式正确的CSV文件"""
    df = pd.read_csv(input_file)
    df['category'] = df['url'].apply(extract_category)
    df = df.rename(columns={'time': 'date'})
    df = df[['title', 'url', 'date', 'category', 'content']]
    df.to_csv(output_file, index=False)
    return df


processed_df = process_csv('filtered_taiwan.csv', 'taiwan-data.csv')

