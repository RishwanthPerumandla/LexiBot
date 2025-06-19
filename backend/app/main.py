from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import upload, ask,summarize,documents,search,validate

app = FastAPI(title="LexiBot API")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LexiBot backend is running 🚀"}


app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(summarize.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(validate.router)  # add this line

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
