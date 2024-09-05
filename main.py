from lyrics_generator import generate_lyrics
from audio_client import generate_and_get_audio

if __name__ == "__main__":
    # 1. 사용자로부터 키워드를 입력받음
    keyword = input("가사 키워드 입력: ")  # 키워드만 입력 받음
    
    # 2. 동요 가사 생성
    lyrics = generate_lyrics(keyword)
    print("생성된 가사:\n", lyrics)
    
    # 3. 태그 및 제목 정의 (필요한 경우 변경 가능)
    tags = "동요, 유아, 키즈"
    title = f"{keyword}에 관한 노래"
    
    # 4. 생성된 가사를 통해 음악을 생성하고 URL을 받아옴
    audio_urls = generate_and_get_audio(lyrics, tags, title, make_instrumental=False, wait_audio=True)

    # 5. 결과로 나온 오디오 URL을 출력
    if audio_urls:
        print("생성된 오디오 URL들:")
        for url in audio_urls:
            print(url)
    else:
        print("오디오 URL을 가져오는 데 실패했습니다.")
