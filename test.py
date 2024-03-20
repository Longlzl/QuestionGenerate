from app import app

# 创建测试客户端
with app.test_client() as client:
    # 准备请求数据
    data = {
        'subject': 'Math',
        'question_type': 'Multiple Choice',
        'difficulty': 'Easy',
        'num_questions': 5,
        'score': 10,
    }

    # 发送POST请求
    response = client.post(
        '/generate_questions',  # 路由
        json=data,  # JSON格式的数据
        content_type='application/json'  # 设置请求头Content-Type为JSON
    )

    # 检查响应状态码
    assert response.status_code == 200  # 假设成功情况下应返回200

    # 解析响应内容并进一步验证
    response_data = response.get_json()
    assert 'questions' in response_data  # 检查响应中是否包含期望的键

    # 其他断言验证，例如验证生成的问题数、格式等