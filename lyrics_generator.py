import time
from openai_client import set_openai_api_key, get_lyrics_from_openai, get_translation_from_openai

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
    lyrics = get_lyrics_from_openai(client, prompt)
    
    # 가사 정리
    lyrics = lyrics.replace('*', '')
    split_lyrics = lyrics.split('\n')
    cleaned_lyrics = ' '.join(''.join(split_lyrics).split())
    
    end = time.time()
    print(f"Processing time: {end - start:.5f} sec")
    
    return cleaned_lyrics

def tag_translation(tag):
    """OpenAI API를 통해 가사를 생성"""
    client = set_openai_api_key()  # OpenAI API 클라이언트 불러오기
    
    start = time.time()
    prompt = f"""
    음악 장르: {tag}

    이 음악 장르를 영어로 번역해줘.
    구분 되는 것이 2개 이상이라면 ',' 쉼표로 구분해주고, 다른 말들은 필요 없이 번역된 말만 답변 해줘.
    """
    
    # OpenAI를 태그 번역
    translated_tag = get_translation_from_openai(client, prompt)
    
    # 태그 정리
    cleaned_tag = 'children song, ' + translated_tag.replace("'", '')
    
    end = time.time()
    print(f"Processing time: {end - start:.5f} sec")
    
    return cleaned_tag
