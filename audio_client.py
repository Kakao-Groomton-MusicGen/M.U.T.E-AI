import time
import requests
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# BASE_URL을 .env에서 불러오기
base_url = os.getenv('BASE_URL')

if base_url is None:
    raise ValueError("BASE_URL이 설정되지 않았습니다. .env 파일을 확인하세요.")

# 오디오 생성 요청 함수
def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    try:
        return response.json()  # JSON 파싱 시도
    except ValueError:
        print("Error: JSON 파싱 실패")
        return None

# 오디오 상태 정보 가져오기 함수
def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    try:
        return response.json()  # JSON 파싱 시도
    except ValueError:
        print("Error: JSON 파싱 실패")
        return None

# 오디오 상태 체크 및 URL 가져오기 함수
def check_audio_status(ids, max_attempts=60, delay=2):
    """오디오 생성 상태를 주기적으로 체크하여 완료되면 URL 반환"""
    for _ in range(max_attempts):
        data = get_audio_information(ids)
        if data and data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            return data[0]['audio_url']
        time.sleep(delay)
    print("Timeout: Audio not available for streaming.")
    return None

# 오디오 생성 및 URL 반환 함수
def generate_and_get_audio(prompt, tags, title, make_instrumental=False, wait_audio=False):
    """노래 가사 및 태그를 통해 오디오 생성 요청 후 URL 반환"""
    # 오디오 생성 요청
    data = custom_generate_audio({
        "prompt": prompt,
        "tags": tags,
        "title": title,
        "make_instrumental": make_instrumental,
        "wait_audio": wait_audio
    })
    
    # 데이터가 없을 경우 처리
    if not data:
        return []

    # 오디오 상태 확인 및 URL 가져오기
    audio_urls = []
    for item in data:
        audio_url = check_audio_status(item['id'])
        if audio_url:
            audio_urls.append(audio_url)
    
    return audio_urls
