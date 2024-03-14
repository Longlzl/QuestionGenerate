import requests
import json

def generate_question(question_type, difficulty, num_questions):
    """
    生成题目

    Args:
        question_type: 题目类型
        difficulty: 题目难度
        num_questions: 题目数量

    Returns:
        题目列表
    """

    # 使用 Gemini API 生成题目
    url = "https://api.gemini.ai/v1/questions"
    params = {
        "api_key": "AIzaSyDRZyWmF6guhBlK-9Vvk3_zTP3VcN1ZuF8",
        "question_type": question_type,
        "difficulty": difficulty,
        "num_questions": num_questions,
    }
    response = requests.get(url, params=params)

    # 解析 API 响应
    if response.status_code == 200:
        data = json.loads(response.content)
        questions = data["questions"]

        return questions

    else:
        raise RuntimeError("API 请求失败:", response.status_code)
