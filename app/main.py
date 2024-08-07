from fastapi import FastAPI
from app.routers import file_processing
import dotenv

dotenv.load_dotenv()

app = FastAPI(
    title="Redact RAG API",
    description="API for Redact RAG",
    version="1.0.0",
)

app.include_router(file_processing.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Redact RAG API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
