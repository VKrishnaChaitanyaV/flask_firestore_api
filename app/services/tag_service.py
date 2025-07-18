from app.repository import tags_repository
from app.models.tag_model import Tag
from typing import List
from datetime import datetime

def get_all_tags() -> List[Tag]:
    return tags_repository.get_all_tags()

def upsert_single_tag(tag_name: str) -> Tag:
    tag_data = tags_repository.upsert_tag(tag_name)
    return Tag(
        tagid="",
        name=tag_data["name"],
        usage_count=1,
        createdAt=datetime.utcnow(),  # Firestore sets actual createdAt
        last_used=datetime.utcnow()
    )

# def upsert_tags_batch(tag_names: List[str]) -> List[Tag]:
#     tag_docs = tags_repository.upsert_tags_batch(tag_names)
#     now = datetime.utcnow()

#     return [
#         Tag(
#             tagid=tag_doc.id,
#             name=tag_doc.to_dict().get("name", ""),
#             usage_count=tag_doc.to_dict().get("usage_count", 1),
#             createdAt=tag_doc.to_dict().get("createdAt", now.isoformat()),
#             last_used=tag_doc.to_dict().get("last_used", now.isoformat())
#         ) for tag_doc in tag_docs if tag_doc.exists
#     ]


def upsert_tags_batch(tag_names: List[str]) -> List[Tag]:
    snapshots = tags_repository.upsert_tags_batch(tag_names)
    now = datetime.utcnow()

    tags = []
    for doc in snapshots:
        data = doc.dict()
        tags.append(Tag(
            tagid=doc.tagid,
            name=data.get("name", ""),
            usage_count=data.get("usage_count", 1),
            createdAt=data.get("createdAt", now.isoformat()),
            last_used=data.get("last_used", now.isoformat())
        ))
    return tags
