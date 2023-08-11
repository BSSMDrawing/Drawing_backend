import os
from flask import Flask, jsonify, request
import openai

app = Flask(__name__)
# OpenAI API 키 설정
openai.api_key = "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"

# ChatGPT와 상호작용하는 함수
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": "You are professional blender programmer"},
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8600, debug=True)
