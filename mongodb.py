from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["MEDITECH_PLANIFAM"]
expediente_medico = db["expediente_medico"]
