from flask import Flask, request, jsonify
from audio_client import generate_and_get_audio  # 오디오 생성 함수 임포트
from lyrics_generator import lyrics_composition

app = Flask(__name__)

# 노래 생성 API 엔드포인트
@app.route('/generate_song', methods=['POST'])
def generate_song():
    # 요청 데이터에서 프롬프트, 태그, 제목 추출
    data = request.get_json()
    
    # 필수 데이터 확인
    prompt = data.get('prompt')
    tags = data.get('tags')
    title = data.get('title')
    
    if not prompt or not tags or not title:
        return jsonify({"error": "프롬프트, 태그, 제목이 모두 필요합니다."}), 400
    
    # 오디오 생성 및 URL 반환
    audio_urls = generate_and_get_audio(prompt, tags, title)
    
    if not audio_urls:
        return jsonify({"error": "오디오 생성 실패"}), 500
    
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

if __name__ == '__main__':
    app.run(debug=True)
