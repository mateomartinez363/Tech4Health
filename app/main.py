from fastapi import FastAPI
app = FastAPI(title = "Tech4Health API")

@app.get("/health")
def health_check():
    return {"status": "ok"}