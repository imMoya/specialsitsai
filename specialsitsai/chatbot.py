from specialsitsai.rag import RAGSystem


class Chatbot:
    """Interactive chatbot for querying the RAGSystem."""
    
    def __init__(self, rag: RAGSystem):
        self.rag = rag
        self.quit_phrases = ["exit", "quit", "bye", "stop"]
    
    def start_chat(self):
        """Starts the interactive loop for asking questions to the RAG system."""
        print("Chatbot is ready. You can start asking questions (type 'exit' to stop).")
        while True:
            user_query = input("You: ")
            if user_query.lower() in self.quit_phrases:
                print("Chatbot: Goodbye!")
                break
            response = self.rag.ask_from_docs(user_query)
            print(f"Chatbot: {response}")
