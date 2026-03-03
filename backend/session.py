from uuid import uuid4
from typing import Set, List

class SessionManager:
    """Manages user sessions for a backend chatbot system.
    
    This module handles session lifecycle including creation, deletion,
    and lookup operations using in-memory storage.
    """
    
    def __init__(self) -> None:
        """Initialize the SessionManager with empty session storage."""
        self._sessions: Set[str] = set()
    
    def create_session(self) -> str:
        """Generate and store a new session.
        
        Returns:
            str: A unique session ID.
        """
        session_id = str(uuid4())
        self._sessions.add(session_id)
        return session_id
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists.
        
        Args:
            session_id: The session ID to check.
        
        Returns:
            bool: True if session exists, False otherwise.
        """
        return session_id in self._sessions
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session if it exists.
        
        Args:
            session_id: The session ID to delete.
        """
        self._sessions.discard(session_id)
    
    def list_sessions(self) -> List[str]:
        """Get all active session IDs.
        
        Returns:
            List[str]: List of active session IDs.
        """
        return list(self._sessions)
    
    def clear_all_sessions(self) -> None:
        """Remove all active sessions."""
        self._sessions.clear()


"""
Usage Example:

    manager = SessionManager()
    
    # Create sessions
    session1 = manager.create_session()
    session2 = manager.create_session()
    
    # Check existence
    assert manager.session_exists(session1) is True
    
    # List sessions
    active = manager.list_sessions()
    assert len(active) == 2
    
    # Delete session
    manager.delete_session(session1)
    assert manager.session_exists(session1) is False
    
    # Clear all
    manager.clear_all_sessions()
    assert len(manager.list_sessions()) == 0
"""