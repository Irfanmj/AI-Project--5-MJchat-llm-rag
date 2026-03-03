from rag import ask_question
from memory import MemoryManager

def test_memory_manager():
    memory = MemoryManager()
    session_id = "test_session"
    
    # Test adding messages
    memory.add_message(session_id, "user", "What is the capital of France?")
    memory.add_message(session_id, "assistant", "The capital of France is Paris.")
    
    # Test retrieving history
    history = memory.get_history(session_id)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "What is the capital of France?"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "The capital of France is Paris."
    
    print("MemoryManager tests passed.")
    

def test_ask_question():
    question = "whats my name?"
    
    answer = ask_question(question,context="")
    
    assert "john" in answer.lower()
    
    print("ask_question tests passed.") 

test_ask_question()
test_memory_manager()
print("All tests passed.")