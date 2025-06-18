import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rishwanthperumandla28:rishi1234@cluster0.e55cg.mongodb.net/LexiBot?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["lexibot"]
documents_collection = db["documents"]
