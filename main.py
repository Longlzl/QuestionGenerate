import os
import google.generativeai as genai
from typing import List, Optional
import json
import pandas as pd
from pandas.io import clipboard


# 建议将API密钥管理逻辑外部化，这里仅作示例
class APIKeyManager:
    @staticmethod
    def get_api_key() -> str:
        # 实际项目中，建议从安全的存储中动态获取API密钥
        return 'AIzaSyBC28DFuinhTiw2xBUOj4DaCT8Tjf6ZG7I'

class QuestionGenerator:
    def __init__(self, proxy: str = 'http://127.0.0.1:7890'):
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        self.api_key = APIKeyManager.get_api_key()
        genai.configure(api_key=self.api_key)

    def generate_question(self, subject: str, question_type: str, difficulty: int, num_questions: int, score: int, knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
        """
        生成题目

        Args:
            subject: 学科
            question_type: 题目类型
            difficulty: 题目难度
            num_questions: 题目数量
            knowledge: 知识点（可缺省）
            tags: 标签（可缺省）
            score: 分值

        Returns:
            题目列表（实际返回的是构建好的prompt字符串）
        """
        if not isinstance(num_questions, int) or num_questions <= 0:
            raise ValueError("num_questions 必须是正整数")
        if not 1 <= difficulty <= 5:
            raise ValueError("difficulty 必须是1到5之间的整数")
        if score < 0:
            raise ValueError("score 必须是非负整数")

        data = {
                "题型": "选择题",
                "题干": "以下哪一项不是导致法国大革命爆发的主要原因？",
                "正确答案": "D",
                "答案解析": "宗教改革与法国大革命的爆发没有直接关系。",
                "分值": 2,
                "难度系数": 2,
                "知识点": "法国大革命",
                "标签": ["法国历史", "社会革命"],
                "A": "专制君主制",
                "B": "社会等级制度",
                "C": "经济危机",
                "D": "宗教改革"
        }
        # 将JSON数据转换为字符串
        json_str = json.dumps(data, ensure_ascii=False, indent=4)

        prompt_pre = f"帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}"
        if knowledge:
            prompt_pre += f", 知识点为{knowledge}"

        if tags:
            prompt_pre += f", 标签为{'、'.join(tags)}"

        prompt = (
            f"{prompt_pre}",
            "其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档",
            "最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及ABCD选项"
            "题目示例："
            f"{json_str}",
        )
        return prompt

    def generate_content(self, prompt: str):
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"生成内容时发生错误: {e}")
            return ""

generator = QuestionGenerator()
prompt = generator.generate_question("历史", "选择题", 3, 3, 2)
response_text = generator.generate_content(prompt)
print(response_text)

# 假设response.text是包含JSON数据的原始文本
json_start = response_text.find('[')
json_end = response_text.rfind(']')

# 提取JSON片段
json_data_str = response_text[json_start:json_end + 1]
print("JSON数据片段:")
print(json_data_str)

# 将打印的 JSON 输出复制到剪贴板
clipboard.copy(json_data_str)
json_str = clipboard.paste()

# 将 JSON 格式的输出保存为文件
with open('output.json', 'w', encoding="utf8") as f:
  f.write(json_str)


# json_data = json.dumps(json_data_str, ensure_ascii=False)
# f2 = open('new_json.json', 'w', encoding="utf8")
# f2.write(json_data)
# f2.close()

# # 假设你有一个非格式化的JSON字符串
# non_formatted_json_str = response_text
#
# # 将其解析为Python对象（字典）
# data = json.loads(non_formatted_json_str)
#
# # 再将Python对象转为格式化后的JSON字符串
# formatted_json_str = json.dumps(data, ensure_ascii=False, indent=4)
# print(formatted_json_str)
