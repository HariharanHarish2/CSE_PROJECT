class ConversationMemory:
    def __init__(self):
        # Stores recent interactions format: [{"role": "user", "content": "..."}, {"role": "system", "sql": "..."}]
        self.history = []
        self.MAX_HISTORY = 5
        
    def add_interaction(self, user_query: str, generated_sql: str):
        self.history.append({"user": user_query, "sql": generated_sql})
        # Keep only last N interactions to prevent prompt bloat
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)
            
    def get_contextualized_prompt(self, new_query: str) -> str:
        """Appends previous history into the prompt to resolve references like 'what about...'"""
        if not self.history:
            return f"User Query: {new_query}"
            
        context_string = "Previous Conversation Context:\n"
        for i, turn in enumerate(self.history):
            context_string += f"Turn {i+1}: User asked '{turn['user']}', System generated '{turn['sql']}'\n"
            
        context_string += f"\nCurrent User Query (Must resolve implied context): {new_query}"
        return context_string

    def clear(self):
        self.history = []
