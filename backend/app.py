from fastapi import FastAPI
from backend.rag import ask_question
from backend.memory import MemoryManager
from backend.session import SessionManager
from backend.context import ContextBuilder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# create application instance
app = FastAPI()
session_manager = SessionManager()
memory_manager = MemoryManager()
context_builder = ContextBuilder()

app.mount("/static", StaticFiles(directory="frontend"))

@app.get("/")
def home():
    """Serve the frontend HTML file."""
    return FileResponse("frontend/index.html")

@app.post("/ask")
def ask(request_data: dict):
        """Handle user questions with session management and context."""
        session_id = request_data.get("session_id")
        question = request_data.get("question")
        
        # Create new session if not provided
        if not session_id:
            session_id = session_manager.create_session()
        
        # Retrieve conversation history
        history = memory_manager.get_history(session_id)
        
        # Build context from history
        context = context_builder.build_context(history)
        
        # Get answer from RAG system
        answer = ask_question(question, context)
        
        # Save to memory
        memory_manager.add_message(session_id, "user", question)
        memory_manager.add_message(session_id, "assistant", answer)
        
        return {
            "answer": answer,
            "session_id": session_id
        }