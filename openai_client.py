import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
def set_openai_api_key():
    """config.env 파일에서 OpenAI API 키 설정"""
    load_dotenv("config.env")  # .env 파일 로드
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 설정되어 있지 않습니다.")
    
    client = OpenAI(api_key=api_key)
    return client

# 메시지를 OpenAI API에 보내서 응답을 받는 함수
def send_prompt_to_openai(client, prompt):
    """주어진 프롬프트로 OpenAI API 호출"""
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": "If you receive a keyword, we will create song lyrics corresponding to it. Please write lyrics according to the song length of 30 seconds to 1 minute."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.5,
        presence_penalty=0.8,
        frequency_penalty=0.8
    )
    return response.choices[0].message.content.strip()
