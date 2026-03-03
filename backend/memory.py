from typing import Dict, List, TypedDict

class Message(TypedDict):
    """Type definition for a message object."""
    role: str
    content: str


class MemoryManager:
    """
    In-memory conversation session store for chatbot backend.
    
    Manages conversation history per session with automatic trimming
    to maintain memory efficiency.
    """

    def __init__(self, max_messages: int = 10) -> None:
        """
        Initialize the memory manager.
        
        Args:
            max_messages: Maximum number of messages to keep per session.
                         Defaults to 10.
        """
        self._storage: Dict[str, List[Message]] = {}
        self._max_messages = max_messages

    def create_session(self, session_id: str) -> None:
        """
        Create a new session if it doesn't already exist.
        
        Args:
            session_id: Unique identifier for the session.
        """
        if session_id not in self._storage:
            self._storage[session_id] = []

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """
        Add a message to a session's conversation history.
        
        Automatically creates the session if it doesn't exist and trims
        history if it exceeds max_messages limit.
        
        Args:
            session_id: Unique identifier for the session.
            role: Message role ("user" or "assistant").
            content: Message content string.
        """
        self.create_session(session_id)
        
        message: Message = {"role": role, "content": content}
        self._storage[session_id].append(message)
        
        self.trim_history(session_id)

    def get_history(self, session_id: str) -> List[Message]:
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: Unique identifier for the session.
            
        Returns:
            List of message objects. Empty list if session doesn't exist.
        """
        return self._storage.get(session_id, [])

    def trim_history(self, session_id: str) -> None:
        """
        Trim session history to keep only the most recent messages.
        
        Maintains the limit specified by max_messages.
        
        Args:
            session_id: Unique identifier for the session.
        """
        if session_id in self._storage:
            if len(self._storage[session_id]) > self._max_messages:
                self._storage[session_id] = self._storage[session_id][
                    -self._max_messages:
                ]

    def clear_session(self, session_id: str) -> None:
        """
        Delete a session and all its conversation history.
        
        Args:
            session_id: Unique identifier for the session.
        """
        if session_id in self._storage:
            del self._storage[session_id]

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists in storage.
        
        Args:
            session_id: Unique identifier for the session.
            
        Returns:
            True if session exists, False otherwise.
        """
        return session_id in self._storage


"""
Usage Example:

    manager = MemoryManager(max_messages=5)
    
    manager.add_message("session_123", "user", "Hello")
    manager.add_message("session_123", "assistant", "Hi there!")
    manager.add_message("session_123", "user", "How are you?")
    
    history = manager.get_history("session_123")
    # Returns: [
    #     {"role": "user", "content": "Hello"},
    #     {"role": "assistant", "content": "Hi there!"},
    #     {"role": "user", "content": "How are you?"}
    # ]
    
    exists = manager.session_exists("session_123")  # Returns: True
    
    manager.clear_session("session_123")
    history = manager.get_history("session_123")  # Returns: []
"""