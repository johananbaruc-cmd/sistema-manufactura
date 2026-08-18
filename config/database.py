import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "sistema_manufactura")

_client = None
_db = None

def get_db():
    """Retorna la instancia de la base de datos (singleton)."""
    global _client, _db
    if _client is None:
        _client = MongoClient(MONGO_URI)
        _db = _client[DB_NAME]
    return _db

def close_db():
    """Cierra la conexión con MongoDB."""
    global _client
    if _client is not None:
        _client.close()
        _client = None