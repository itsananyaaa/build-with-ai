from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routes (make sure folder structure is correct)
from app.api.routes import auth, persona, chat, voice, memory, agent

# Initialize FastAPI app
app = FastAPI(
    title="PersonaAI Backend",
    description="Multi-persona adaptive intelligent assistant.",
    version="1.0.0"
)

# CORS Middleware (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router)
app.include_router(persona.router)
app.include_router(chat.router)
app.include_router(voice.router)
app.include_router(memory.router)
app.include_router(agent.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "PersonaAI Backend System is running. See /docs for API details."
    }

# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )