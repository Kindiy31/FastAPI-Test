from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    DB_USER: str = "Graintrack"
    DB_PASSWORD: str = "Graintrack_test"
    DB_NAME: str = "graintrack"

    DB_URL: str = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"

    class Config:
        case_sensitive = True


settings = Settings()
