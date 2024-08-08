import pymongo
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Conectar a MongoDB utilizando la URI de .env
client = pymongo.MongoClient(os.getenv("MONGO_URI"))

# Obtener la base de datos
db_name = os.getenv("MONGO_DB_NAME", "gestDep_db_json")
db = client[db_name]

# Obtener la colección
collection_name = os.getenv("MONGO_COLLECTION_MATCH", "match_URU")
collection = db[collection_name]

def get_db_m():
    return db
