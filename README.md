# LangChain + pgvector FastAPI RAG 서버 with Next.js 챗봇

이 프로젝트는 LangChain과 pgvector를 사용한 FastAPI 기반 RAG (Retrieval-Augmented Generation) API 서버와 Next.js 챗봇 프론트엔드입니다.

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 설정

```bash
# 필요한 파일들이 준비되어 있는지 확인
ls -la
# app/, frontend/, Dockerfile, docker-compose.yaml, requirements.txt 등이 있어야 합니다
```

### 2. 환경 변수 설정

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

### 4. 애플리케이션 접속

애플리케이션이 실행되면 다음 URL로 접속할 수 있습니다:

- **챗봇 UI**: http://localhost:3000
- **API 문서 (Swagger UI)**: http://localhost:8000/docs
- **대체 API 문서 (ReDoc)**: http://localhost:8000/redoc
- **헬스체크**: http://localhost:8000/health
- **루트 엔드포인트**: http://localhost:8000/

## 📋 구성 요소

### 서비스

- **postgres**: pgvector 확장이 포함된 PostgreSQL 16 데이터베이스
- **langchain_app**: FastAPI 기반 RAG API 서버
- **frontend**: Next.js 기반 챗봇 UI
- **pgadmin**: 데이터베이스 관리 도구 (선택사항)

### 주요 파일 및 디렉토리

- `app/api_server.py`: FastAPI 메인 서버 (사용자 제공 코드 스타일)
- `frontend/`: Next.js 챗봇 프론트엔드
  - `frontend/app/`: Next.js App Router 페이지
  - `frontend/components/`: React 컴포넌트
  - `frontend/lib/`: API 클라이언트 및 유틸리티
- `Dockerfile`: FastAPI 앱용 Docker 이미지 정의
- `frontend/Dockerfile`: Next.js 앱용 Docker 이미지 정의
- `docker-compose.yaml`: 전체 서비스 오케스트레이션
- `requirements.txt`: Python 의존성 패키지
- `init-db.sql`: PostgreSQL 초기화 스크립트

## 🔧 기능

### 1. RESTful API
- FastAPI 기반의 현대적인 웹 API
- 자동 API 문서화 (Swagger UI, ReDoc)
- 타입 검증 및 자동 직렬화

### 2. 벡터 검색 API (`/retrieve`)
- pgvector를 사용한 유사도 검색
- 검색 결과에 유사도 점수 포함

### 3. RAG 질의 API (`/rag`)
- OpenAI API를 사용한 실제 AI 응답 생성
- 참조된 문서 목록 반환

### 4. 문서 관리 API
- `POST /documents`: 단일 문서 추가
- `POST /documents/batch`: 여러 문서 일괄 추가

### 5. Next.js 챗봇 UI
- 실시간 채팅 인터페이스
- 참조 문서 표시
- 반응형 디자인
- Tailwind CSS 스타일링

### 6. 헬스체크 API (`/health`)
- 서비스 상태 확인
- 데이터베이스 연결 상태 확인
- RAG 체인 초기화 상태 확인

## 🛠️ 개발 및 디버깅

### 로컬 개발 (Docker 없이)

#### 백엔드 (FastAPI)
```bash
cd app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드 (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### 컨테이너 상태 확인

```bash
# 모든 컨테이너 상태 확인
docker-compose ps

# 특정 서비스 로그 확인
docker-compose logs postgres
docker-compose logs langchain_app
docker-compose logs frontend

# 컨테이너 내부 접속
docker-compose exec postgres psql -U langchain_user -d langchain_db
docker-compose exec langchain_app bash
docker-compose exec frontend sh
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

## 🔍 API 엔드포인트

### 주요 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 루트 엔드포인트 (API 정보) |
| GET | `/health` | 헬스체크 |
| POST | `/retrieve` | 벡터 유사도 검색 |
| POST | `/rag` | RAG 질의 |
| POST | `/documents` | 단일 문서 추가 |
| POST | `/documents/batch` | 여러 문서 일괄 추가 |
| GET | `/docs` | Swagger UI 문서 |
| GET | `/redoc` | ReDoc 문서 |

### 요청/응답 예시

#### RAG 질의 요청
```json
{
  "question": "LangChain이 무엇인가요?",
  "k": 3
}
```

#### RAG 질의 응답
```json
{
  "question": "LangChain이 무엇인가요?",
  "answer": "LangChain은 LLM 애플리케이션을 구축하기 위한 강력한 프레임워크입니다...",
  "retrieved_documents": [
    {
      "content": "LangChain은 LLM 애플리케이션을 구축하기 위한 강력한 프레임워크입니다.",
      "metadata": {"source": "demo"}
    }
  ],
  "retrieved_count": 1
}
```

## 🛑 종료

```bash
# 모든 서비스 종료
docker-compose down

# 볼륨까지 함께 삭제 (데이터 초기화)
docker-compose down -v
```

## 📝 주의사항

1. **OpenAI API 키**: RAG 기능을 사용하려면 반드시 필요합니다. `.env` 파일에 설정하세요.
2. **데이터 지속성**: PostgreSQL 데이터는 Docker 볼륨에 저장되어 컨테이너 재시작 후에도 유지됩니다.
3. **포트 충돌**:
   - 3000(Next.js), 8000(FastAPI), 5432(PostgreSQL), 8080(pgAdmin) 포트가 이미 사용 중이면 docker-compose.yaml에서 포트를 변경하세요.
4. **개발 모드**: 로컬에서 개발할 때는 각 서비스를 개별적으로 실행할 수 있습니다.

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

### Next.js 빌드 오류
```bash
# 프론트엔드 컨테이너 재빌드
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### API 서버 접속 불가
```bash
# 컨테이너 로그 확인
docker-compose logs langchain_app

# 포트 확인
docker-compose ps

# 컨테이너 재시작
docker-compose restart langchain_app
```

### CORS 오류
- `app/api_server.py`에서 CORS 설정을 확인하세요.
- 프론트엔드와 백엔드가 같은 네트워크에 있는지 확인하세요.
