import pymongo

# MongoDB Database 
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['bihar_tender']
mycol = mydb["tender_data"]

global mongo

# mongo = mycol.insert_many(df)
# print(mongo.inserted_ids)
# print(type(mongo))