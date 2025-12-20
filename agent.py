import os
import sys
import ollama  # Official Ollama library
import faiss   # Vector Database
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
from sqlalchemy import create_engine

# --- CONFIGURATION ---
DB_URL = 'postgresql://user:password@localhost:5432/taxidata'
MODEL_NAME = "qwen2:0.5b"  # Or "phi3" if you prefer
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class LocalAgent:
    def __init__(self):
        print(">>> 🧠 Initializing Embeddings (Sentence-Transformers)...")
        # Load the embedding model directly
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.documents = []

    def load_data(self):
        print(">>> 📂 Loading data from PostgreSQL...")
        engine = create_engine(DB_URL)
        try:
            df = pd.read_sql("SELECT * FROM location_metrics LIMIT 100", engine)
        except Exception as e:
            print(f"❌ DB Error: {e}")
            sys.exit(1)

        print(f">>> 📝 Found {len(df)} records. processing...")
        
        # Convert rows to text
        self.documents = []
        for _, row in df.iterrows():
            text = (
                f"Location ID {row['location_id']} stats: "
                f"Avg Dist: {row['avg_dist']:.2f} miles. "
                f"Trips: {row['trip_count']}. "
                f"Avg Cost: ${row['avg_cost']:.2f}."
            )
            self.documents.append(text)

        # Create Embeddings
        print(">>> 🔢 Creating vectors (this uses your CPU)...")
        embeddings = self.embedder.encode(self.documents)
        
        # Store in FAISS (The Vector DB)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))
        print(">>> ✅ Knowledge Base Built!")

    def query(self, user_question):
        # 1. Embed the user's question
        q_embed = self.embedder.encode([user_question])
        
        # 2. Search FAISS for the 3 most relevant data points
        k = 3
        distances, indices = self.index.search(np.array(q_embed), k)
        
        # 3. Retrieve the actual text
        context_lines = [self.documents[i] for i in indices[0]]
        context_block = "\n".join(context_lines)
        
        # --- DEBUG PRINT (Add this!) ---
        print("\n" + "="*30)
        print(f"🧐 AI FOUND THESE CLUES:")
        print(context_block)
        print("="*30 + "\n")
        # -------------------------------
        
        # 4. Construct the prompt
        # We will make the prompt SIMPLER for the small model
        prompt = f"""
        Context information is below.
        ---------------------
        {context_block}
        ---------------------
        Given the context information and not prior knowledge, answer the query.
        Query: {user_question}
        Answer:
        """
        
        # 5. Send to Ollama
        print(">>> 🤔 Thinking...")
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        return response['message']['content']

def main():
    agent = LocalAgent()
    agent.load_data()
    
    print("\n" + "="*40)
    print(f"   🤖 PURE PYTHON AGENT ({MODEL_NAME})")
    print("="*40)
    
    while True:
        q = input("\nYou: ")
        if q.lower() in ["exit", "quit"]:
            break
            
        try:
            answer = agent.query(q)
            print(f"Agent: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Make sure the Ollama app is running!")

if __name__ == "__main__":
    main()