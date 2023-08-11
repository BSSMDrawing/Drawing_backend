import requests

# 서버 URL 설정
server_url = "http://localhost:8600/chat"

# 클라이언트로부터 질문 입력 받기
prompt = input("Enter your question: ")

# POST 요청을 보내서 서버와 대화하기
response = requests.post(server_url, json={'prompt': prompt})

# 서버로부터 받은 JSON 응답 처리
if response.status_code == 200:
    data = response.json()
    print("Server response:", data['response'])
else:
    print("Error:", response.json())