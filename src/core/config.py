# thirdparty
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# fastapi
from pydantic import Field

DOTENV_PATH = find_dotenv(".env")
load_dotenv(DOTENV_PATH)


class AppSettings(BaseSettings):
    api_production: bool = Field(default=True)
    echo_queries: bool = Field(default=False)

    # Main Postgres
    db_user: str = Field(default="postgres")
    db_password: str = Field(default="pass")
    db_host: str = Field(default="db")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="pattern_db")

    # Test Postgres
    test_db_user: str = Field(default="postgres_test")
    test_db_password: str = Field(default="pass_test")
    test_db_host: str = Field(default="db_test")
    test_db_port: int = Field(default=5432)
    test_db_name: str = Field(default="pattern_db_test")

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_path(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def test_database_path(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.test_db_user}:{self.test_db_password}@{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"
        )


settings = AppSettings()
