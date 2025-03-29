class Settings:
    # Database settings
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    DB_ECHO: bool = True

    # Server settings
    URL: str = "127.0.0.1:8000"
    API_PREFIX: str = "/api"
    
    # Static files settings
    STATIC_DIR: str = "static/"
    
    #Yandex OAuth settings
    YANDEX_CLIENT_ID: str = "603fcc97e1544065beaeeaaeb9af1f4a"
    YANDEX_CLIENT_SECRET: str = "36c3ea40e34e40bea2adc66113f0cd8f"
    YANDEX_REDIRECT_URL: str = "http://localhost:8000/auth/yandex/callback"
    
    # JWT settings
    ALGHORITHM: str = "HS256"
    SECRET_KEY: str = "default"
    ACCESS_TOKEN_EXPIRE: int = 60 * 24 * 7  # 7 days

# Create an instance of the Settings class
settings = Settings()
