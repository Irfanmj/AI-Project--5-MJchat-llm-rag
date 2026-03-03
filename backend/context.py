"""
Context module for formatting conversation history into LLM prompt context.

This module converts stored conversation history into formatted text context
for a language model without calling any external APIs or models.
"""


class ContextBuilder:
    """
    Builds formatted prompt context from conversation history.
    
    Converts a list of message dictionaries into a readable dialogue string
    suitable for LLM input.
    
    Example usage:
        builder = ContextBuilder(max_messages=6)
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        context = builder.build_context(history)
    """
    
    def __init__(self, max_messages: int = 6) -> None:
        """
        Initialize ContextBuilder.
        
        Args:
            max_messages: Maximum number of recent messages to include in context.
                         Defaults to 6.
        """
        self.max_messages = max_messages
    
    def build_context(self, history: list[dict]) -> str:
        """
        Build formatted context string from conversation history.
        
        Args:
            history: List of message dictionaries with 'role' and 'content' keys.
            
        Returns:
            Formatted dialogue string ready for LLM input.
        """
        limited_messages = self.limit_messages(history)
        formatted_lines = [
            self.format_message(msg["role"], msg["content"])
            for msg in limited_messages
        ]
        return "\n".join(formatted_lines)
    
    def format_message(self, role: str, content: str) -> str:
        """
        Format a single message into readable string.
        
        Args:
            role: Message role ('user' or 'assistant').
            content: Message content text.
            
        Returns:
            Formatted message line.
        """
        role_label = role.capitalize()
        return f"{role_label}: {content}"
    
    def limit_messages(self, history: list[dict]) -> list[dict]:
        """
        Trim conversation history to maximum recent messages.
        
        Args:
            history: Full conversation history.
            
        Returns:
            Trimmed list of messages based on max_messages limit.
        """
        return history[-self.max_messages:]
    
    def count_tokens_estimate(self, text: str) -> int:
        """
        Estimate token count using simple word count approximation.
        
        Useful for debugging and logging purposes. Provides rough estimate
        where 1 token ≈ 0.75 words.
        
        Args:
            text: Text to estimate tokens for.
            
        Returns:
            Estimated token count.
        """
        words = len(text.split())
        return int(words / 0.75)