"""FastAPI 메인 애플리케이션."""

import asyncio
import psycopg2
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.models import HealthResponse
from app.api.routes import search, rag
from app.core.vectorstore import initialize_vectorstore


def wait_for_postgres() -> None:
    """PostgreSQL 데이터베이스가 준비될 때까지 대기."""
    import time

    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=settings.postgres_host,
                port=settings.postgres_port,
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password,
            )
            conn.close()
            print("✅ PostgreSQL 데이터베이스 연결 성공!")
            return
        except psycopg2.OperationalError:
            retry_count += 1
            print(f"⏳ PostgreSQL 연결 대기 중... ({retry_count}/{max_retries})")
            time.sleep(2)

    raise Exception("PostgreSQL 데이터베이스에 연결할 수 없습니다.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 함수."""
    # 시작 시
    print("🚀 FastAPI RAG 애플리케이션 시작 중...")
    wait_for_postgres()
    print("🔧 벡터스토어 초기화 중...")
    initialize_vectorstore()
    print("✅ 애플리케이션 준비 완료!")
    yield
    # 종료 시
    print("👋 애플리케이션 종료 중...")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="LangChain과 pgvector를 사용한 RAG API 서버",
    lifespan=lifespan,
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(search.router)
app.include_router(rag.router)


@app.get("/", tags=["root"])
async def root() -> dict:
    """루트 엔드포인트."""
    return {
        "message": "LangChain RAG API에 오신 것을 환영합니다!",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    """헬스체크 엔드포인트."""
    try:
        # 데이터베이스 연결 확인
        conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
        )
        conn.close()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        database=db_status,
        openai_configured=settings.openai_api_key is not None,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )

