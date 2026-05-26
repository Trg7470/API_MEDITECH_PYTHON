from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["MEDITECH_PLANIFAM"]
expediente_medico = db["Expediente_Medico"]

def convert_bson(data):

    if isinstance(data, list):
        return [convert_bson(item) for item in data]

    if isinstance(data, dict):
        return {
            key: convert_bson(value)
            for key, value in data.items()
        }

    if isinstance(data, ObjectId):
        return str(data)

    if isinstance(data, Decimal128):
        return float(data.to_decimal())

    return data