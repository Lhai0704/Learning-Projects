import pandas as pd


def merge_columns(input_file, output_file):
    """
    将CSV文件中detailed_description列的内容拼接到synopsis列后面，
    然后删除detailed_description列并保存结果

    Parameters:
    input_file (str): 输入CSV文件路径
    output_file (str): 输出CSV文件路径
    """
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 确保两列都存在
    if 'synopsis' not in df.columns or 'detailed_description' not in df.columns:
        raise ValueError("CSV文件必须包含'synopsis'和'detailed_description'列")

    # 将detailed_description的内容拼接到synopsis后面
    # 使用fillna('')确保处理空值
    df['synopsis'] = df['synopsis'].fillna('') + ' ' + df['detailed_description'].fillna('')

    # 删除detailed_description列
    df = df.drop('detailed_description', axis=1)

    # 保存结果到新的CSV文件
    df.to_csv(output_file, index=False)

    return df


# 使用示例
input_file = 'Casadellibro_data.csv'
output_file = 'data.csv'

merged_df = merge_columns(input_file, output_file)