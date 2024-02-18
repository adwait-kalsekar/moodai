from pymongo import MongoClient

client = MongoClient('mongodb+srv://kalsekaradwait:supersecretpassword@cluster0.lmzj7j7.mongodb.net/?retryWrites=true&w=majority')
db = client['ezbuy']
collection = db['test']