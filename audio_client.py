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
def check_audio_status(ids, max_attempts=60, delay=5):
    """오디오 생성 상태를 주기적으로 체크하여 완료되면 URL 반환"""

    audio_url = []

    for _ in range(max_attempts):
        data = get_audio_information(ids)
        
        # 반환된 데이터가 리스트가 아닌 경우 바로 종료
        if not data:
            print("Error: 서버로부터 데이터를 받아오지 못했습니다.")
            return None

        if data[0]["status"] == 'streaming' or data[0]["status"] == 'complete':
            audio_url.append(data[0]['audio_url'])
            audio_url.append(data[1]['audio_url'])
            return audio_url

        # # 리스트로 반환된 경우
        # if isinstance(data, list) and len(data) > 0:
        #     first_item = data[0]  # 첫 번째 아이템을 확인
        #     if 'status' in first_item and first_item['status'] == 'streaming':
        #         return first_item['audio_url']
        
        # # 딕셔너리로 반환된 경우
        # elif isinstance(data, dict) and 'status' in data and data['status'] == 'streaming':
        #     print(f"{data['id']} ==> {data['audio_url']}")
        #     return data['audio_url']
        
        time.sleep(delay)
    
    print("Timeout: Audio not available for streaming.")
    return None

# 오디오 파일 다운로드 함수
def download_audio(audio_url, file_name):
    """주어진 URL에서 오디오 파일을 다운로드하여 저장"""
    response = requests.get(audio_url)
    if response.status_code == 200:
        # AI-Model/music_output 폴더에 파일 저장
        output_dir = "AI-Model/music_output"
        os.makedirs(output_dir, exist_ok=True)  # 폴더가 없으면 생성
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"파일이 성공적으로 다운로드되었습니다: {file_path}")
    else:
        print(f"오류 발생: {response.status_code}")

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

    # 크레딧이 없는 경우
    if data is None:
        print("Error: API 응답이 없습니다. 크레딧을 확인하세요.")
        return []
    
    # 오류가 있는 경우 처리
    if "error" in data:
        print(f"Error: {data['error']}")
        return []

    ids = f"{data[0]['id']},{data[1]['id']}"
    audio_url = check_audio_status(ids)

    # audio_urls = []    

    # # 여러 개의 오디오 파일을 처리
    # for item in data[:2]:  # 2개의 오디오만 처리하도록 제한
    #     if isinstance(item, dict) and "id" in item:
    #         audio_url = check_audio_status(item['id'])
    #         if audio_url:
    #             audio_urls.append(audio_url)
    #             # 오디오 파일 다운로드
    #             download_audio(audio_url, f"{item['id']}.mp3")
    #     else:
    #         print(f"Unexpected item format or missing 'id': {item}")
    
    return audio_urls
