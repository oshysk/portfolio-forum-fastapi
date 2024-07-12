from fastapi import FastAPI

from src.routers import forum
from src.routers import comment

# MEMO: 仮実装
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(forum.router)
app.include_router(comment.router)

# MEMO: 仮実装
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
