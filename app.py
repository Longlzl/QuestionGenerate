from flask import Flask, request, jsonify
from main import QuestionGenerator
import json

app = Flask(__name__)

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    subject = data.get['subject']
    question_type = data.get['question_type']
    difficulty = data.get['difficulty']
    num_questions = data.get['num_questions']
    score = data.get['score']
    knowledge = data.get('knowledge')
    tags = data.get('tags')

    generator = QuestionGenerator()
    prompt = generator.generate_question(subject, question_type, difficulty, num_questions, score, knowledge, tags)
    response_text = generator.generate_content(prompt)

    # 提取JSON数据并返回
    json_start = response_text.find('[')
    json_end = response_text.rfind(']')
    if json_start != -1 and json_end != -1:
        json_data_str = response_text[json_start:json_end + 1]
        try:
            questions = json.loads(json_data_str)
            return jsonify(questions)
        except ValueError:
            return jsonify({"error": "无法解析JSON数据"}), 500
    else:
        return jsonify({"error": "未找到有效JSON数据"}), 500

if __name__ == '__main__':
    app.run(debug=True)
