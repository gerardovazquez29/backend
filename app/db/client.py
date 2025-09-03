from pymongo import MongoClient

db_client = MongoClient().local


# Base de datos Remota
# db_client = MongoClient(
# "mongodb+srv://<usuario>:<contraseña>@cluster0.mongodb.net/test?retryWrites=true&w=majority"
# ).test