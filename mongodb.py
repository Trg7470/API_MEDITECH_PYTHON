from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["MEDITECH_PLANIFAM"]
expediente_medico = db["Expediente_Medico"]
