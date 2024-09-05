import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv('BASE_URL')

def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

# 상태 체크 및 오디오 URL 가져오기 함수
def check_audio_status(ids, max_attempts=60, delay=2):
    for _ in range(max_attempts):
        data = get_audio_information(ids)
        for audio_data in data:
            if audio_data["status"] == 'streaming':
                print(f"{audio_data['id']} ==> {audio_data['audio_url']}")
                return audio_data['audio_url']
        time.sleep(delay)
    print("Timeout: Audio not available for streaming.")
    return None

def generate_and_get_audio(prompt, tags, title, make_instrumental=False, wait_audio=False):
    # 오디오 생성 요청
    data = custom_generate_audio({
        "prompt": prompt,
        "tags": tags,
        "title": title,
        "make_instrumental": make_instrumental,
        "wait_audio": wait_audio
    })
    
    # 오디오 상태 확인 및 URL 가져오기
    audio_urls = []
    audio_url_1 = check_audio_status(data[0]['id'])
    if audio_url_1:
        audio_urls.append(audio_url_1)
        
    audio_url_2 = check_audio_status(data[1]['id'])
    if audio_url_2:
        audio_urls.append(audio_url_2)
        
    return audio_urls