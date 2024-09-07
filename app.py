# app.py
from flask import Flask, request, jsonify, send_file, Response
from audio_client import generate_and_get_audio  # 오디오 생성 함수 임포트
from lyrics_generator import lyrics_composition, tag_translation
from music_uploader import upload_music
from werkzeug.utils import secure_filename
import os
from config import BASE_URL, SWAGGER_URL

app = Flask(__name__)

# BASE_URL과 SWAGGER_URL 확인
print(f"BASE URL: {BASE_URL}")
print(f"Swagger URL: {SWAGGER_URL}")

# 노래 생성 API 엔드포인트
@app.route('/generate_song', methods=['POST'])
def generate_song():
    # 요청 데이터에서 keywords, style, title 추출
    data = request.get_json()
    
    keywords = data.get('keywords')
    style = data.get('style')
    title = data.get('title')
    
    if not keywords or not style or not title:
        return jsonify({"error": "prompt, tags, title이 모두 필요합니다."}), 400
    
    style_translated = tag_translation(style)  # 태그(스타일) 번역
    
    # 오디오 생성 및 URL 반환
    try:
        audio_urls = generate_and_get_audio(keywords, style_translated, title)
    except Exception as e:
        print(f"오디오 생성 중 에러 발생: {e}")
        return jsonify({"error": "오디오 생성 중 문제가 발생했습니다."}), 500

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

    # 오디오 파일을 스트리밍 방식으로 다운로드
    response = requests.get(audio_url, stream=True)

    if response.status_code == 200:
        # 파일을 스트리밍 방식으로 클라이언트에 제공
        return Response(
            response.iter_content(chunk_size=10 * 1024),  # 10KB씩 스트리밍
            content_type=response.headers.get('Content-Type', 'application/octet-stream'),
            headers={'Content-Disposition': 'attachment; filename=temp_audio_file.mp3'}
        )
    else:
        return jsonify({"error": f"오디오 다운로드 실패: {response.status_code}"}), 500

# 노래 s3에 업로드
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "File이 필요합니다."}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "File 이름이 비어있습니다."}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(filename)

        # S3에 업로드하고 URL을 받아옴
        response, status_code = upload_music(filename)

        return jsonify(response), status_code
    else:
        return jsonify({"error": "File이 존재하지 않습니다. hello world"}), 400

if __name__ == '__main__':
    app.run(debug=True)
