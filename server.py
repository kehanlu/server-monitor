from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from device import NvidiaSMI, RAM

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://140.118.127.80:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https?:\/\/.*\.ntust\.edu\.tw",
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origin_regex="https?:\/\/.*\.ntust\.edu\.tw",
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 


@app.get("/")
async def root():
    return {
        "nvidia_smi": NvidiaSMI(),
        "ram": RAM()
    }
