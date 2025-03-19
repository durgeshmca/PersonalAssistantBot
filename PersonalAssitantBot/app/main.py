from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import  auth_router
from app.routers.users import users_router
from app.routers.chats import chat_router

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)
