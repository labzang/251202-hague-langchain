# LangChain + pgvector Hello World

이 프로젝트는 LangChain과 pgvector를 사용한 간단한 벡터 검색 애플리케이션입니다.

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 설정

```bash
# 필요한 파일들이 준비되어 있는지 확인
ls -la
# app.py, Dockerfile, docker-compose.yaml, requirements.txt 등이 있어야 합니다
```

### 2. 환경 변수 설정 (선택사항)

OpenAI API를 사용하려면 환경 변수를 설정하세요:

```bash
# env.example을 .env로 복사
cp env.example .env

# .env 파일을 편집하여 OpenAI API 키 설정
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Docker 컨테이너 실행

```bash
# 모든 서비스 시작 (백그라운드)
docker-compose up -d

# 또는 로그를 보면서 실행
docker-compose up

# pgAdmin도 함께 실행하려면
docker-compose --profile admin up -d
```

### 4. 애플리케이션 테스트

```bash
# LangChain 앱 컨테이너에 접속
docker-compose exec langchain_app python app.py

# 또는 로그 확인
docker-compose logs -f langchain_app
```

## 📋 구성 요소

### 서비스

- **postgres**: pgvector 확장이 포함된 PostgreSQL 16 데이터베이스
- **langchain_app**: LangChain Hello World 애플리케이션
- **pgadmin**: 데이터베이스 관리 도구 (선택사항)

### 주요 파일

- `app.py`: LangChain + pgvector 연동 메인 애플리케이션
- `Dockerfile`: LangChain 앱용 Docker 이미지 정의
- `docker-compose.yaml`: 전체 서비스 오케스트레이션
- `requirements.txt`: Python 의존성 패키지
- `init-db.sql`: PostgreSQL 초기화 스크립트

## 🔧 기능

### 1. 벡터 검색
- pgvector를 사용한 유사도 검색
- 샘플 문서들이 자동으로 임베딩되어 저장됨

### 2. RAG (Retrieval-Augmented Generation)
- OpenAI API 키가 있으면 실제 AI 응답 생성
- API 키가 없어도 벡터 검색 기능은 정상 작동

### 3. 대화형 인터페이스
- 콘솔에서 직접 질문하고 답변 받기
- 실시간 벡터 검색 결과 확인

## 🛠️ 개발 및 디버깅

### 컨테이너 상태 확인

```bash
# 모든 컨테이너 상태 확인
docker-compose ps

# 특정 서비스 로그 확인
docker-compose logs postgres
docker-compose logs langchain_app

# 컨테이너 내부 접속
docker-compose exec postgres psql -U langchain_user -d langchain_db
docker-compose exec langchain_app bash
```

### 데이터베이스 확인

```bash
# PostgreSQL에 직접 연결
docker-compose exec postgres psql -U langchain_user -d langchain_db

# pgvector 확장 확인
\dx

# 테이블 목록 확인
\dt
```

### pgAdmin 사용 (선택사항)

1. `docker-compose --profile admin up -d`로 실행
2. 브라우저에서 `http://localhost:8080` 접속
3. 로그인: `admin@example.com` / `admin`
4. 서버 추가:
   - Host: `postgres`
   - Port: `5432`
   - Database: `langchain_db`
   - Username: `langchain_user`
   - Password: `langchain_password`

## 🔍 테스트 질문 예시

애플리케이션이 실행되면 다음과 같은 질문들을 테스트해볼 수 있습니다:

- "LangChain이 무엇인가요?"
- "pgvector는 어떤 기능을 제공하나요?"
- "Docker의 장점은 무엇인가요?"
- "Python이 AI 개발에 인기 있는 이유는?"

## 🛑 종료

```bash
# 모든 서비스 종료
docker-compose down

# 볼륨까지 함께 삭제 (데이터 초기화)
docker-compose down -v
```

## 📝 주의사항

1. **OpenAI API 키**: 없어도 벡터 검색은 작동하지만, 실제 AI 응답을 위해서는 필요합니다.
2. **데이터 지속성**: PostgreSQL 데이터는 Docker 볼륨에 저장되어 컨테이너 재시작 후에도 유지됩니다.
3. **포트 충돌**: 5432(PostgreSQL), 8080(pgAdmin) 포트가 이미 사용 중이면 docker-compose.yaml에서 포트를 변경하세요.

## 🚨 문제 해결

### PostgreSQL 연결 실패
```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose logs postgres

# 헬스체크 확인
docker-compose ps
```

### Python 패키지 오류
```bash
# 컨테이너 재빌드
docker-compose build --no-cache langchain_app
docker-compose up -d
```

### 권한 문제
```bash
# 볼륨 권한 확인 및 재설정
docker-compose down -v
docker-compose up -d
```
