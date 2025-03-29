class Settings:
    # Database settings
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    DB_ECHO: bool = True

    # Server settings
    URL: str = "127.0.0.1:8000"
    API_PREFIX: str = "/api"


# Create an instance of the Settings class
settings = Settings()
