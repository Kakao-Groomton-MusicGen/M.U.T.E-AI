import time
import tiktoken
from openai_client import set_openai_api_key, send_prompt_to_openai

# 동요 가사 생성 함수
def generate_lyrics(keyword):
    """OpenAI API를 통해 가사를 생성"""
    client = set_openai_api_key()  # API 키는 openai_client.py에서 자동으로 불러옴
    
    start = time.time()
    prompt = f"""
    키워드 {keyword}에 관련된 동요 가사를 만들어줘.
    한글 가사, 노래의 장르는 동요, 노래의 길이는 30초~1분 정도 길이로 부탁해.
    [Verse]
    [Chorus]
    [Outro]
    """
    
    lyrics = send_prompt_to_openai(client, prompt)
    split_lyrics = lyrics.split('\n')
    cleaned_lyrics = ' '.join(''.join(split_lyrics).split())
    
    end = time.time()
    print(f"Processing time: {end - start:.5f} sec")
    
    return cleaned_lyrics