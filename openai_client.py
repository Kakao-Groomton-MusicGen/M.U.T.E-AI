import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
def set_openai_api_key():
    """.env 파일에서 OpenAI API 키 설정"""
    load_dotenv(".env")  # .env 파일 로드
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 설정되어 있지 않습니다.")
    
    client = OpenAI(api_key=api_key)
    return client

# 메시지를 OpenAI API에 보내서 응답을 받는 함수
def send_prompt_to_openai(client, prompt):
    """주어진 프롬프트로 OpenAI API 호출"""
    system_content = """
    You are a creative lyricist specializing in children's songs. The user will provide a keyword, and your task is to create a song with simple, fun, and repetitive lyrics in the following structure:

    1. [Verse] - Simple and imaginative lyrics based on the keyword, easy for children to follow.
    2. [Chorus] - Repetitive and catchy section that children can easily remember and sing along to.
    3. [Outro] - A closing part that wraps up the song in a cheerful and playful manner.

    The lyrics should be light, positive, and appropriate for a children's song. Ensure the language is simple, playful, and easy for children to understand. Use rhyme and repetition to make it fun and memorable.
    """

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.5,
        presence_penalty=0.8,
        frequency_penalty=0.8
    )
    return response.choices[0].message.content.strip()
