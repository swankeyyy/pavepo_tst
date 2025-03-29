import uvicorn
from fastapi import FastAPI


# Initialize FastAPI app
app = FastAPI(
    title="AudioFY",
    description="Test task for PAVEPO, a service for storing and processing audio files with yandex authorization",
    version="0.0.1",
    contact={
        "name": "Ivan Levchuk",
        "email": "swankyyy1@gmail.com",
    },
    docs_url="/",
    redoc_url=None,
)


# Run the app with uvicorn server
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
