# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# ipconfig
from fastapi import FastAPI
from pydantic import *

app = (
    FastAPI())

di = "uncirculate"
a = ''
@app.get("/phymo")
def motor_receive(motor: int):
    global di
    di = "clockwise" if motor == 1 else "counterclockwise" if motor == -1 else "uncirculate"
    print(di)
    return "success"

@app.get("/phymo/rasp")
def read_motor():
    global di
    return di