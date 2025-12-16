"""애플리케이션 설정 관리."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정."""

    # 데이터베이스 설정
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "langchain_db")
    postgres_user: str = os.getenv("POSTGRES_USER", "langchain_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "langchain_password")

    # OpenAI 설정
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")

    # 애플리케이션 설정
    app_name: str = "LangChain RAG API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    @property
    def database_url(self) -> str:
        """데이터베이스 연결 문자열 반환."""
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    class Config:
        """Pydantic 설정."""

        env_file = ".env"
        case_sensitive = False


settings = Settings()

