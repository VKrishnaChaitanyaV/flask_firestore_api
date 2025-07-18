from app.repository import user_repository
from app.models.user_model import User
from datetime import datetime

def create_user(user_data):
    user_data['createdAt'] = datetime.utcnow().isoformat()
    user_data['updatedAt'] = datetime.utcnow().isoformat()
    user = User(**user_data)
    return user_repository.create_user(user.dict())

def get_user(userid):
    doc = user_repository.get_user_by_id(userid)
    return doc.to_dict() if doc.exists else None

def update_user(userid, user_data):
    user_data['updatedAt'] = datetime.utcnow().isoformat()
    existing = get_user(userid)
    if not existing:
        return None
    updated_data = {**existing, **user_data}
    user = User(**updated_data)  # validate merged data
    return user_repository.update_user(userid, user_data)


def delete_user(userid):
    return user_repository.delete_user(userid)

def list_all_users():
    return user_repository.list_users()