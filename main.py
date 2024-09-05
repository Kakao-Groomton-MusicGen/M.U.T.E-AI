# main.py
from lyrics_generator import generate_lyrics

if __name__ == "__main__":
    keyword = input("가사 키워드 입력: ")  # 키워드만 입력 받음
    lyrics = generate_lyrics(keyword)
    print("Generated Lyrics:\n", lyrics)