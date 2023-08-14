import os
import re
from flask import Flask, jsonify, request
import openai
import requests

app = Flask(__name__)
# OpenAI API 키 설정
openai.api_key = os.getenv("OPEN_API_KEY")

with open("assistant.txt", "r", encoding="utf-8") as file:
    input_text = file.read()

# ChatGPT와 상호작용하는 함수
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": "You are professional blender programmer"},
            {"role": "assistant", "content": input_text},
            {"role": "user", "content": prompt},
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

# ChatGPT와 대화하는 엔드포인트
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if 'prompt' not in data:
        return jsonify({'error': 'Prompt is required'}), 400

    prompt = data['prompt']
    response = chat_with_gpt(prompt)

    # JSON 형식으로 응답 보내기
    return jsonify({'response': response})

code_server_url = "http://other_server_url/code_endpoint"

@app.route('/process_code', methods=['POST'])
def process_code():
    data = request.json
    if 'response' not in data:
        return jsonify({'error': 'Response is required'}), 400

    response_text = data['response']

    # 정규식을 사용하여 코드 블럭 추출
    code_blocks = re.findall(r"```[\s\S]*?```", response_text)

    # 코드 블럭을 다른 서버에 전송할 형식에 맞게 조합 및 전송
    for idx, code_block in enumerate(code_blocks):
        code_block = code_block.strip("```")  # 코드 블럭의 ``` 제거
        code_data = {"id": f"code_{idx}", "value": code_block}

        # code_data를 다른 서버로 전송
        code_response = requests.post(code_server_url, json=code_data)

        if code_response.status_code == 200:
            print(f"Code {idx} sent successfully")
        else:
            print(f"Error sending code {idx} to the other server")

    return jsonify({'message': 'Code processing completed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8600, debug=True)
