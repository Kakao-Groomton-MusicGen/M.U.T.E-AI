import time
from openai_client import set_openai_api_key, send_prompt_to_openai

# 동요 가사 생성 함수
def lyrics_composition(keyword):
    """OpenAI API를 통해 가사를 생성"""
    client = set_openai_api_key()  # OpenAI API 클라이언트 불러오기
    
    start = time.time()
    prompt = f"""
    키워드: {keyword}

    이 키워드를 바탕으로 가사를 작성해줘. [Verse], [Chorus], [Outro] 형식으로 부탁해.
    노래의 장르는 동요고, 노래 길이 30초에서 1분정도에 맞춰서 가사를 작성해줘.
    """
    
    # OpenAI를 통해 가사 생성
    lyrics = send_prompt_to_openai(client, prompt)
    
    # 가사 정리
    lyrics = lyrics.replace('*', '')
    split_lyrics = lyrics.split('\n')
    cleaned_lyrics = ' '.join(''.join(split_lyrics).split())
    
    end = time.time()
    print(f"Processing time: {end - start:.5f} sec")
    
    return cleaned_lyrics
