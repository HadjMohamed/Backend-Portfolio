from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb import Client
from flask import Flask, request, jsonify
from flask_cors import CORS  
import json
import os


app = Flask(__name__)

# PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
# CORS_ORIGIN = f"https://{PUBLIC_DOMAIN}" if PUBLIC_DOMAIN else "http://127.0.0.1:5500"

# CORS
CORS(app, resources={r"/chatbot": {"origins": ["https://hadjmohamed.github.io",
                                               "http://127.0.0.1:5500"
                                               ]}})

def init_database():
    
    # Embedding Model : MiniLM
    embedding_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Sentence-BERT model

    # Chroma DB creation or loading
    client = Client()
    
    # Try to load the existing collection
    persist_dir = os.path.join(os.path.dirname(__file__), 'data/vector_db')
    json_path=os.path.join(os.path.dirname(__file__), 'data/personal-data2.json')

    # Loading JSON and creating new collection
    with open(json_path, 'r') as file:
        data = json.load(file)

    TEXT = [f"{item['question']} {item['answer']}" for item in data]
    meta_data = [{"question": item["question"], "answer": item["answer"]} for item in data]
    ids = [f"doc_{i}" for i in range(len(TEXT))]

    vector_db = Chroma.from_texts(
        texts=TEXT,
        embedding=embedding_func,
        metadatas=meta_data,
        persist_directory=persist_dir, 
        collection_name="questions_reponses"
)
            
    return vector_db

vectordb=init_database()
    
def generate_humanized_response(query):

    # Similarity search
    response = vectordb.similarity_search_with_score(query=query, k=5)
    best_match, similarity_score = response[0]
    if response : #Only relevant answers
        answer = best_match.metadata.get('answer')
        response = f"Merci pour votre question ! {answer}."
    else:
        response = "Je suis désolé, je n'ai pas pu trouver d'informations correspondant à votre question dans la base de données. N'hésitez pas à poser une autre question ou à contacter directement Mohamed."

    return response

# Flask app

@app.route('/')
def home():
    return "API online !"

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_input = data.get("question", "")
    response = generate_humanized_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
