# Flask 주소록 애플리케이션

간단하고 직관적인 Flask 기반 주소록 웹 애플리케이션입니다. 사용자 친화적인 인터페이스로 연락처 정보를 쉽게 관리할 수 있습니다.

## 주요 기능
- **연락처 관리**: 추가, 수정, 삭제 기능
<img src="https://github.com/gomtam/image/blob/main/250521/%EC%A3%BC%EC%86%8C%EB%A1%9D-%ED%99%88-05-21-2025_05_05_PM.png" width="700">
- **검색 기능**: 이름, 전화번호 등으로 빠른 검색
- <img src="https://github.com/gomtam/image/blob/main/250521/%EC%A3%BC%EC%86%8C%EB%A1%9D-%ED%99%88-05-21-2025_05_05_PM%20(1).png" width="700">
- **사진 첨부**: 연락처에 사진 추가 가능
- <img src="https://github.com/gomtam/image/blob/main/250521/%EC%A3%BC%EC%86%8C%EB%A1%9D-%EC%97%B0%EB%9D%BD%EC%B2%98-%EC%88%98%EC%A0%95-05-21-2025_04_47_PM.png" width="700">
- **반응형 디자인**: 모바일 및 데스크톱 환경 모두 지원

## 설치 방법

### 1. 저장소 복제
```bash
git clone https://github.com/gomtam/flaskjuso-camera.git
cd flaskjuso-camera
```

### 2. 가상 환경 설정
```bash
# Conda 사용 시
conda create -n flaskjuso-camera python=3.9
conda activate flaskjuso-camera

# venv 사용 시
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

1. 애플리케이션 서버 실행:
```bash
python jusoApp002.py
```

2. 웹 브라우저에서 접속:
```
http://127.0.0.1:5000
```

## 기술 스택

- **백엔드**: Python 3.x, Flask
- **데이터 저장**: 텍스트 파일 기반 (addrbook.txt)
- **프론트엔드**: HTML, CSS, JavaScript
- **이미지 처리**: 기본 이미지 처리 기능 포함

## 프로젝트 구조

```
flaskjuso-camera/
├── jusoApp002.py      # 메인 애플리케이션 파일
├── addrbook.txt       # 연락처 데이터 저장 파일
├── static/
│   ├── images/        # 사용자 사진 저장 디렉토리
│   └── style.css      # 스타일시트
├── templates/         # HTML 템플릿 디렉토리
└── requirements.txt   # 필요 패키지 목록
```

## 라이센스

MIT 라이센스에 따라 사용할 수 있습니다. 
