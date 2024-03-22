from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello root!"}

@app.get("/home")
def home():
    return {"message": "Home!"}