from app import db
from app.config import Config
from datetime import datetime
from app.models.tag_model import Tag
from typing import List, Optional

tags_collection = db.collection(Config.TAGS_COLLECTION)

def get_all_tags():
    return [doc.to_dict() for doc in tags_collection.stream()]

def get_tag_by_id(tagid: str) -> Optional[Tag]:
    doc_ref = tags_collection.document(tagid.lower())
    doc = doc_ref.get()
    if doc.exists:
        return Tag(tagid=doc.id, **doc.to_dict())
    return None

def get_tag_by_name(substring: str) -> List[Tag]:
    substring = substring.strip().lower()
    if not substring:
        return []

    docs = tags_collection.stream()
    return [
        Tag(tagid=doc.id, **doc.to_dict())
        for doc in docs
        if substring in doc.id
    ]

# def upsert_tag(tag_name: str) -> dict:
#     tag_id = tag_name.strip().lower()
#     doc_ref = tags_collection.document(tag_id)
#     doc = doc_ref.get()

#     if doc.exists:
#         doc_ref.update({
#             "usage_count": 1,#firestore.Increment(1),
#             "last_used": datetime.utcnow().isoformat()
#         })
#     else:
#         doc_ref.set({
#             "name": tag_name.strip(),
#             "usage_count": 1,
#             "createdAt": datetime.utcnow().isoformat(),
#             "last_used": datetime.utcnow().isoformat()
#         })

#     return {"tagid": tag_id, "name": tag_name.strip()}

def upsert_tag(name: str) -> Tag:
    tagid = name.strip().lower()
    now = datetime.utcnow().isoformat()
    doc_ref = tags_collection.document(tagid)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({
            "usage_count": 1, #doc.get("usage_count", 0)+1,
            "last_used": now
        })
        existing = doc.to_dict()
        return Tag(
            tagid=tagid,
            name=existing.get("name", name.strip()),
            usage_count=existing.get("usage_count", 1) + 1,
            createdAt=existing.get("createdAt", now),
            last_used=now
        )
    else:
        tag_data = Tag(
            tagid=tagid,
            name=name.strip(),
            usage_count=1,
            createdAt=now,
            last_used=now
        )
        doc_ref.set(tag_data.dict(exclude={"tagid"}))
        return tag_data


def upsert_tags_batch(tag_names: List[str]) -> List[Tag]:
    # Normalize and deduplicate tags
    tag_names = [name.strip().lower() for name in tag_names if name.strip()]
    tag_names = list(set(tag_names))
    
    now = datetime.utcnow()
    batch = db.batch()

    # Create references for documents we need to upsert
    tag_docs = {name: tags_collection.document(name) for name in tag_names}
    existing_docs = db.get_all(tag_docs.values())

    result = []
    print("Processing tags...")

    for doc, name in zip(existing_docs, tag_names):
        doc_ref = tag_docs[name]
        
        if doc.exists:  # Check if document exists
            existing = doc.to_dict()  # Get existing document data
            print(f"Updating tag: {name}")
            
            # Update the document with the usage count and last used timestamp
            batch.update(doc_ref, {
                "usage_count": existing.get("usage_count", 0) + 1,  # Increment usage count
                "last_used": now
            })

            # Create Tag object for result
            result.append(Tag(
                tagid=existing.get("tagid"),
                name=existing.get("name", name),
                usage_count=existing.get("usage_count", 0) + 1,
                createdAt=existing.get("createdAt", now),
                last_used=now
            ))
        else:
            print(f"Creating new tag: {name}")
            # If the document doesn't exist, create a new one
            doc_ref = tags_collection.document(name)
            tag = Tag(
                tagid=doc_ref.id,
                name=name,
                usage_count=1,
                createdAt=now,
                last_used=now
            )
            
            # Set the new tag document
            batch.set(doc_ref, tag.dict())
            result.append(tag)

    # Commit the batch operation
    batch.commit()

    return result


