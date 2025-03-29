import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2


from api import router as api_router

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

# Import and include routers
app.include_router(api_router)


# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Run the app with uvicorn server
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
