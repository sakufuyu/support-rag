from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str | None = None
    database_host: str | None = None
    database_port: int = 5432
    database_name: str = "support_rag"
    database_username: str | None = None
    database_password: str | None = None

    access_code: str = "demo-access-code"

    class Config:
        env_file = ".env"

    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if not all([
            self.database_host,
            self.database_username,
            self.database_password,
        ]):
            raise ValueError("Database configuration is incomplete.")

        return (
            f"postgresql+psycopg://{self.database_username}:"
            f"{self.database_password}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )

settings = Settings()
