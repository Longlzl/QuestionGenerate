import os
import json
import pandas as pd
import google.generativeai as genai
from typing import List, Optional

# 建议将API密钥管理逻辑外部化
class APIKeyManager:
    @staticmethod
    def get_api_key() -> str:
        # 实际项目中，建议从安全的存储中动态获取API密钥
        # 例如从环境变量中获取
        return os.getenv('API_KEY', 'AIzaSyBC28DFuinhTiw2xBUOj4DaCT8Tjf6ZG7I')

class QuestionGenerator:
    def __init__(self, proxy: str = 'http://127.0.0.1:7890'):
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        self.api_key = APIKeyManager.get_api_key()
        genai.configure(api_key=self.api_key)

    def _build_prompt(self, subject: str, question_type: str, difficulty: int, num_questions: int, score: int, knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
        """
        构建生成题目的prompt字符串
        """
        data = {
            "题型": "选择题",
            "题干": "以下哪一项不是导致法国大革命爆发的主要原因？",
            "正确答案": "D",
            "答案解析": "宗教改革与法国大革命的爆发没有直接关系。",
            "分值": 2,
            "难度系数": 2,
            "知识点": "法国大革命",
            "标签": "法国历史",
            "A": "专制君主制",
            "B": "社会等级制度",
            "C": "经济危机",
            "D": "宗教改革"
        }
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        prompt_pre = f"帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}"
        if knowledge:
            prompt_pre += f", 知识点为{knowledge}"
        if tags:
            prompt_pre += f", 标签为{'、'.join(tags)}"
        prompt = (
            f"{prompt_pre}",
            "其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档",
            "最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及A、B、C、D选项",
            "题目示例：",
            f"{json_str}",
        )
        return prompt

    def generate_question(self, subject: str, question_type: str, difficulty: int, num_questions: int, score: int, knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
        """
        生成题目
        """
        # 参数校验可以进一步增强，这里仅示例基本检查
        if not isinstance(num_questions, int) or num_questions <= 0:
            raise ValueError("num_questions 必须是正整数")
        if not 1 <= difficulty <= 5:
            raise ValueError("difficulty 必须是1到5之间的整数")
        if score < 0:
            raise ValueError("score 必须是非负整数")

        prompt = self._build_prompt(subject, question_type, difficulty, num_questions, score, knowledge, tags)
        return prompt

    def generate_content(self, prompt: str):
        try:
            model = genai.GenerativeModel('gemini-pro')
            # 使用代理
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"生成内容时发生错误: {e}")
            return ""

# 使用优化后的代码进行题目生成和处理
generator = QuestionGenerator()
prompt = generator.generate_question("历史", "选择题", 3, 3, 2)
response_text = generator.generate_content(prompt)
print(response_text)

# 提取和处理JSON数据应确保异常处理机制完备
try:
    json_start = response_text.find('[')
    json_end = response_text.rfind(']')
    if json_start == -1 or json_end == -1:
        raise ValueError("无法找到有效的JSON数据")
    json_data_str = response_text[json_start:json_end + 1]
    # 将JSON数据写入文件前先进行合法性验证
    json.loads(json_data_str)  # 若解析失败，会抛出ValueError异常
    with open('output.json', 'w', encoding="utf8") as f:
        f.write(json_data_str)
except ValueError as ve:
    print(f"处理JSON数据时出错: {ve}")

else:
    # 尝试解析JSON片段
    try:
        with open('output.json', 'r', encoding="utf8") as f:
            data = json.load(f)
        # 将JSON数据转换为DataFrame
        df = pd.DataFrame(data)
        # 写入Excel文件
        with pd.ExcelWriter('generated_questions.xlsx') as writer:
            df.to_excel(writer, index=False, sheet_name='Questions')
        print("已成功将生成的题目写入'generated_questions.xlsx'文件中。")
    except Exception as e:
        print(f"写入Excel文件时发生错误: {e}")
    # 如果有需要，还可以添加一个finally子句，用于进行资源清理等操作
