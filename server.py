from fastapi import FastAPI
from device import NvidiaSMI, RAM

app = FastAPI()


@app.get("/")
async def root():
    return {
        "nvidia_smi": NvidiaSMI(),
        "ram": RAM()
    }
