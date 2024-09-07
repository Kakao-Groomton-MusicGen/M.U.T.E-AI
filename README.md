# M.U.T.E - Music Understanding Teaching Education

**M.U.T.E**는 사용자가 입력한 키워드를 기반으로 AI가 맞춤형 노래를 생성하여 교육적 이해와 학습을 돕는 플랫폼입니다.

![image](https://github.com/user-attachments/assets/c1f81d69-6928-4e23-934c-d99dc888f6b1)

---

## 프로젝트 개요

M.U.T.E는 **Music**(음악), **Understanding**(이해), **Teaching**(가르침), **Education**(교육)을 의미하며, 음악을 통해 더 나은 학습 경험을 제공하고 교육적 이해를 향상시키는 것을 목표로 합니다.

---

## 팀 소개

**TEMU**(Team + Music)는 기술과 교육을 음악으로 연결하는 혁신적인 음악 생성 서비스를 제공하기 위해 노력하고 있습니다.

---

# AI 기반 동요 생성 프로젝트

이 프로젝트는 어린이를 위한 교육적인 노래를 생성하는 AI 서비스입니다. 사용자가 입력한 가사, 노래 스타일, 제목을 바탕으로 AI가 가사를 생성하고 음악을 만들어주는 기능을 제공합니다.

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [AI 기술 스택](#AI-기술-스택)
- [설치 방법](#설치-방법)
- [사용법](#사용법)
- [API 엔드포인트](#api-엔드포인트)
- [파일 구조](#파일-구조)
- [라이센스](#라이센스)

## 프로젝트 개요
이 프로젝트는 사용자로부터 키워드, 노래 스타일, 제목 등의 입력을 받아 AI로 가사를 생성한 후, 음악을 생성합니다. 생성된 음악 파일은 다운로드 또는 스트리밍이 가능합니다.

### 작업 흐름
1. 사용자가 노래에 대한 키워드, 스타일, 제목을 입력합니다.
2. AI 모델이 입력된 키워드를 기반으로 가사를 생성합니다.
3. 생성된 가사를 바탕으로 음악이 생성됩니다.
4. 생성된 오디오 파일의 URL을 반환하고, 사용자는 이를 다운로드하거나 스트리밍할 수 있습니다.

## 주요 기능
- **가사 생성**: 사용자가 입력한 키워드를 바탕으로 자동으로 가사를 생성합니다.
- **음악 생성**: 생성된 가사를 기반으로 AI 모델을 통해 음악을 만듭니다.
- **커스텀 스타일**: 어린이 동요 등 다양한 스타일을 선택할 수 있습니다.
- **오디오 다운로드**: 생성된 오디오 파일의 URL을 제공하여 다운로드 또는 스트리밍이 가능합니다.
- **에러 처리**: 크레딧 부족, 서버 타임아웃 등의 문제를 처리하는 에러 핸들링 기능을 포함합니다.

## AI 기술 스택
| **Language** | **LLM**  | **API** | **Model** |
| -------------- | -------- | ---------------- | ---------------- |
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | ![Openai](https://img.shields.io/badge/OpenAI-412991.svg?style=for-the-badge&logo=OpenAI&logoColor=white) | ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) | ![SUNO](https://img.shields.io/badge/Suno-000000.svg?style=for-the-badge&logo=Suno&logoColor=white) |

- **OpenAI GPT-4o mini**: 가사 생성에 사용됩니다. 사용자가 입력한 키워드와 스타일을 바탕으로 자연스러운 가사를 만들어냅니다.
- **Suno AI 모델:** Suno의 음악 생성 AI API를 활용하여 가사를 기반으로 음악을 만듭니다. 다양한 음악 스타일과 템포를 조정할 수 있는 커스텀 기능을 제공합니다.
- **Flask API**: 백엔드 서버에서 AI 모델과 클라이언트 간의 통신을 처리하는 역할을 하며, 사용자로부터 입력을 받아 AI 모델로 전달합니다.
- **음성 합성 기술**: 생성된 가사를 실제 오디오 파일로 변환하는 데 사용되며, Suno AI를 통해 음성 합성 및 음성 모델링을 제공합니다.

### AI 모델 세부 사항:
- **OpenAI GPT**: 사용자의 키워드와 스타일에 맞춰 자연어 처리(NLP)를 통해 가사를 생성하는 역할을 담당합니다.
- **Suno AI**: Suno의 AI 모델을 이용해 음악 및 음성 생성에 특화된 서비스로, AI 기반으로 실제 음악 트랙을 구성하고 오디오 파일을 제공합니다.


## 설치 방법

### 요구 사항
- Python 3.9 이상
- Flask
- Requests
- dotenv
- validators
- Git

### 설치 단계
1. 이 저장소를 클론합니다:
   ```bash
   git clone https://github.com/your-repo/ai-generated-childrens-songs.git
   cd ai-generated-childrens-songs
   ```

2. 필요한 패키지를 설치합니다:
   ```bash
   pip install -r requirements.txt
   ```

3. 환경 변수 설정:
   - 프로젝트 루트 디렉토리에 `.env` 파일을 생성한 후, Suno API의 BASE_URL과 필요한 환경 변수를 추가합니다.
   ```bash
   BASE_URL=http://3.38.173.206:3000
   ```

4. 프로젝트 실행:
   ```bash
   python main.py
   ```

## 사용법
### 애플리케이션 실행
1. 프로그램을 실행한 후, 노래의 키워드, 스타일, 제목을 입력합니다.
2. 시스템이 입력한 키워드를 바탕으로 가사를 생성합니다.
3. 생성된 가사를 바탕으로 음악을 생성하고, 오디오 URL을 제공합니다.

### 예시:
```bash
$ python main.py
가사 키워드 입력 : 야구
노래 스타일 입력 : 동요
제목 입력 : 야구

Processing time: 1.95362 sec
생성된 가사:
 [Verse] 작은 공이 툭 튕겨, 야구장으로 가자! 배트로 쳐서 날려봐, 하늘 높이 날아가!

생성된 오디오 URL들:
https://audio.example.com/song1.mp3
https://audio.example.com/song2.mp3
```

## API 엔드포인트
다음은 프로젝트에서 사용할 수 있는 API 엔드포인트 목록입니다:

- **`/api/generate`**: 음악을 생성합니다.
- **`/api/custom_generate`**: 설정된 가사, 스타일, 제목을 바탕으로 커스텀 음악을 생성합니다.
- **`/api/generate_lyrics`**: 키워드를 바탕으로 가사를 생성합니다.
- **`/api/get`**: 음악 목록을 조회합니다.
- **`/api/get?ids=`**: 특정 ID로 음악 정보를 조회합니다.
- **`/api/get_limit`**: API 사용량 정보를 조회합니다.
- **`/api/extend_audio`**: 음악 길이를 연장합니다.
- **`/api/concat`**: 연장된 오디오를 연결하여 완성된 음악을 생성합니다.

## 파일 구조
```
.
├── app.py                     # 애플리케이션 진입점
├── audio_client.py             # 음악 생성 API 요청 처리
├── lyrics_generator.py         # 가사 생성 처리
├── config.py                   # 환경 변수와 설정 관리
├── requirements.txt            # 필요한 Python 패키지 목록
├── .env                        # 환경 변수 (.env 파일)
└── README.md                   # 이 README 파일
```

## 라이센스
이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
