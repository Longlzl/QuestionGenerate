import pandas as pd
import json


# 尝试解析JSON片段
try:
    with open('output.json', 'r', encoding="utf8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"无法解析JSON数据: {e}")
else:
    # 将JSON数据转换为DataFrame
    df = pd.DataFrame(data)

    # 写入Excel文件
    with pd.ExcelWriter('generated_questions.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='Questions')

    print("已成功将生成的题目写入'generated_questions.xlsx'文件中。")
