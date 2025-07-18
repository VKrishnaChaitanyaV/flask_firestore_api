from app import db
from app.config import Config

collection = db.collection(Config.USER_COLLECTION)

def create_user(data):
    doc_ref = collection.document()     
    data['userid'] = doc_ref.id        
    doc_ref.set(data)                   
    return data                         

def get_user_by_id(userid):
    return collection.document(userid).get()

def update_user(userid, data):
    data.pop("userid", None) 
    return collection.document(userid).update(data)

def delete_user(userid):
    return collection.document(userid).update({"active": False})

def list_users():
    return [doc.to_dict() for doc in collection.stream()]