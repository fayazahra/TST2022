from pymongo import MongoClient
connect = MongoClient('mongodb://asteresrh:zaahirah21@ac-igfzzlb-shard-00-00.1iohpll.mongodb.net:27017,ac-igfzzlb-shard-00-01.1iohpll.mongodb.net:27017,ac-igfzzlb-shard-00-02.1iohpll.mongodb.net:27017/?ssl=true&replicaSet=atlas-i19dru-shard-0&authSource=admin&retryWrites=true&w=majority')

db = connect.TubesTST
userDB = db["User"]
diabetesDB = db["model_input"]