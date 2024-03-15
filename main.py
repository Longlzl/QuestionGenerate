import os
import google.generativeai as genai

# Initialize the Generative AI client
os.environ['GEMINI_API_KEY'] = 'AIzaSyBC28DFuinhTiw2xBUOj4DaCT8Tjf6ZG7I'
proxy = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['http_proxy'] = proxy
os.environ['https_proxy'] = proxy

api_key = 'AIzaSyBC28DFuinhTiw2xBUOj4DaCT8Tjf6ZG7I'
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def generate_question(subject, question_type, difficulty, num_questions, score, knowledge=None, tags=None):
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

    # 检查输入参数合法性
    if not isinstance(num_questions, int) or num_questions <= 0:
        raise ValueError("num_questions 必须是正整数")
    prompt_pre = "帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}".format(num_questions=num_questions, subject=subject, question_type=question_type, difficulty=difficulty, score=score)
    if knowledge:
        prompt_pre += ", 知识点为{}".format(knowledge)

    if tags:
        prompt_pre += ", 标签为{}".format(tags)
    prompt = ("{prompt_pre}",
              "其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档",
              "最终结果以json形式输出，包括题型、题干、正确答案、答案解析、分值、难度系数、知识点、标签以及ABCD选项,示例如下：",
              {
                  "parts": [
                      {
                          "题型": "选择题",
                          "题干": "已知函数 f(x) = x^2 - 4x + 3，下列哪个选项是 f(x) 的一个零点？",
                          "inline_data": {
                              "正确答案": "A",
                              "答案解析": "要求函数的零点，即求解 f(x) = 0，代入选项中的值，只有当 x = 1 时，f(1) = 1^2 - 4*1 + 3 = 0，所以 x = 1 是函数 f(x) 的一个零点。",
                              "分值": 1,
                              "难度系数": 2,
                              "知识点": "二次函数的零点",
                              "标签": ["数学", "选择题", "二次函数"],
                              "选项": {
                                  "A": "x = 1",
                                  "B": "x = 2",
                                  "C": "x = 3",
                                  "D": "x = 4"
                              },
                          }
                      }
                  ]
              })
    return prompt

prompt = generate_question("历史", "选择题", 3,3,2)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(prompt)
print(response.text)
