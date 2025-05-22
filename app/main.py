from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import topic, models, files

app = FastAPI(title="Smart Learning Assistant (SLAS)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(topic.router)
app.include_router(models.router)
app.include_router(files.router)


@app.get("/")
async def root():
    """Root endpoint for the SLAS API."""

    return {"message": "SLAS is up and running!"}
