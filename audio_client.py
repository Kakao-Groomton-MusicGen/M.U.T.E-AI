# audio_client.py
import time
import requests
from dotenv import load_dotenv
import os
from config import BASE_URL  # config.py에서 BASE_URL 가져오기

# 오디오 생성 요청 함수
def custom_generate_audio(payload):
    
    url = f"{BASE_URL}/api/custom_generate"  # API 엔드포인트 변경
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    print(f"Request sent to {url} with payload: {payload}")  # 요청 로그 추가
    try:
        return response.json()  # JSON 파싱 시도
    except ValueError:
        print("Error: JSON 파싱 실패")
        print(f"Response content: {response.content}")  # 응답 내용 출력
        return None

# 오디오 상태 정보 가져오기 함수
def get_audio_information(audio_ids):
    url = f"{BASE_URL}/api/get?ids={audio_ids}" # BASE_URL을 사용
    print(f"Checking audio status for IDs: {audio_ids}")  # 상태 체크 로그 추가
    response = requests.get(url)
    try:
        return response.json()  # JSON 파싱 시도
    except ValueError:
        print("Error: JSON 파싱 실패")
        print(f"Response content: {response.content}")  # 응답 내용 출력
        return None


# 오디오 상태 체크 및 URL 가져오기 함수 (디버깅 정보 추가)
def check_audio_status(ids, max_attempts=60, delay=5):
    """오디오 생성 상태를 주기적으로 체크하여 완료되면 URL 반환"""
    
    audio_url = []

    for attempt in range(max_attempts):
        print(f"Checking audio status... Attempt {attempt + 1} of {max_attempts}")
        data = get_audio_information(ids)

        # 데이터가 없을 경우 바로 종료
        if not data:
            print("Error: 서버로부터 데이터를 받아오지 못했습니다.")
            return None

        # 상태 확인 디버깅
        statuses = [item["status"] for item in data]
        print(f"Current statuses: {statuses}")

        # 상태가 'streaming' 또는 'complete'일 때 URL 반환
        if all(status in ['streaming', 'complete'] for status in statuses):
            for item in data:
                if "audio_url" in item and item["audio_url"]:
                    audio_url.append(item['audio_url'])
            if audio_url:
                return audio_url

        # 지정된 지연 시간 후 재시도
        print("Audio generation still in progress, waiting for completion...")
        time.sleep(delay)
    
    print("Timeout: Audio not available for streaming after maximum attempts.")
    return None

    # # 리스트로 반환된 경우
    # if isinstance(data, list) and len(data) > 0:
    #     first_item = data[0]  # 첫 번째 아이템을 확인
    #     if 'status' in first_item and first_item['status'] == 'streaming':
    #         return first_item['audio_url']
        
    # # 딕셔너리로 반환된 경우
    # elif isinstance(data, dict) and 'status' in data and data['status'] == 'streaming':
    #     print(f"{data['id']} ==> {data['audio_url']}")
    #     return data['audio_url']
        
# 오디오 파일 다운로드 함수
def download_audio(audio_url, file_name):
    """주어진 URL에서 오디오 파일을 다운로드하여 저장"""
    response = requests.get(audio_url)
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        # AI-Model/music_output 폴더에 파일 저장
        output_dir = "AI-Model/music_output"  # 절대 경로 대신 상대 경로 사용
        os.makedirs(output_dir, exist_ok=True)  # 폴더가 없으면 생성
        file_path = os.path.join(output_dir, file_name)

        print(f"Saving file to: {file_path}")  # 저장 경로 출력
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"파일이 성공적으로 다운로드되었습니다: {file_path}")
    else:
        print(f"오류 발생: {response.status_code}")

# 오디오 생성 및 URL 반환 함수
def generate_and_get_audio(prompt, tags, title, make_instrumental=False, wait_audio=False):
    """노래 가사 및 태그를 통해 오디오 생성 요청 후 URL 반환"""
    # 오디오 생성 요청
    print(f"Sending request with prompt: {prompt}, tags: {tags}, title: {title}")
    # 딕셔너리가 아니라 개별 인자로 전달
    payload = {
        "prompt": prompt,
        "tags": tags,
        "title": title,
        "make_instrumental": make_instrumental,
        "wait_audio": wait_audio  # Set to False for background processing
    }

    # 오디오 생성 요청 (wait_audio=False)
    data = custom_generate_audio(payload)

    # 크레딧이 없는 경우
    if data is None:
        print("Error: API 응답이 없습니다. 크레딧을 확인하세요.")
        return []

    # 바이트 스트링 응답을 JSON으로 변환 (필요 시)
    if isinstance(data, bytes):
        try:
            data = data.decode('utf-8')  # 바이트 스트링을 UTF-8로 디코딩
            data = json.loads(data)      # JSON으로 파싱
        except (ValueError, UnicodeDecodeError) as e:
            print(f"Error while decoding JSON: {e}")
            return []

    # 오류가 있는 경우 처리
    if "error" in data:
        print(f"Error: {data['error']}")
        return []

    # 응답에서 audio_url을 추출
    audio_urls = []
    for item in data:
        if "audio_url" in item and item["audio_url"]:
            audio_urls.append(item["audio_url"])

    if audio_urls:
        print(f"오디오 URL: {audio_urls}")
        return audio_urls
    else:
        print("오디오 URL을 가져오는 데 실패했습니다.")
        return []

    # song_id 추출
    print(f"API 응답 데이터: {data}")
    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"Audio generation IDs: {ids}")

    # 상태 체크 후 완료되면 URL 반환
    audio_urls = check_audio_status(ids)


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
    
    return audio_url
