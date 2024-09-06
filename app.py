from flask import Flask, request, jsonify
from audio_client import generate_and_get_audio  # 오디오 생성 함수 임포트
from lyrics_generator import lyrics_composition, tag_translation

app = Flask(__name__)

# 노래 생성 API 엔드포인트
@app.route('/generate_song', methods=['POST'])
def generate_song():
    # 요청 데이터에서 프롬프트, 태그, 제목 추출
    data = request.get_json()
    
    prompt = data.get('prompt')
    tags = data.get('tags')
    title = data.get('title')
    
    if not prompt or not tags or not title:
        return jsonify({"error": "프롬프트, 태그, 제목이 모두 필요합니다."}), 400
    
    tags = tag_translation(tags)

    # 오디오 생성 및 URL 반환
    audio_urls = generate_and_get_audio(prompt, tags, title)
    
    if not audio_urls:
        return jsonify({"error": "오디오 생성 실패"}), 500
    
    # URL만 제공
    return jsonify({"audio_urls": audio_urls}), 200

# 가사 생성 API 엔드포인트
@app.route('/generate_lyrics', methods=['POST'])
def generate_lyrics():
    data = request.get_json()

    keyword = data.get('keyword')

    if not keyword:
        return jsonify({"error": "키워드가 필요합니다."}), 400

    lyrics = lyrics_composition(keyword)

    if not lyrics:
        return jsonify({"error": "가사 생성 실패"}), 500

    return jsonify({"lyrics": lyrics}), 200

# 오디오 다운로드 API 엔드포인트
@app.route('/download_audio', methods=['POST'])
def download_audio():
    data = request.get_json()

    # 요청 데이터에서 audio_url 추출
    audio_url = data.get('audio_url')

    if not audio_url:
        return jsonify({"error": "오디오 URL이 필요합니다."}), 400

    # 오디오 파일 다운로드
    response = requests.get(audio_url)
    
    if response.status_code == 200:
        # 파일을 임시로 저장하고 클라이언트에 제공
        file_name = f"temp_audio_file.mp3"
        with open(file_name, 'wb') as file:
            file.write(response.content)
        
        # Flask의 send_file을 사용하여 파일을 클라이언트에 전달
        return send_file(file_name, as_attachment=True)
    else:
        return jsonify({"error": f"오디오 다운로드 실패: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
