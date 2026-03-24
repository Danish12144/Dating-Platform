# app/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.client import get_db
from app.models.chat import Message
from app.schemas import chat as chat_schema
from app.routes.users import get_current_user_id
from app.utils.pagination import pagination_params

router = APIRouter(tags=["chat"])


@router.post("/chat/send", response_model=chat_schema.MessageResponseSchema)
async def send_message(
    payload: chat_schema.MessageCreateSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    # TODO: add block/check logic later
    msg = await Message.send(
        db,
        from_user=user_id,
        to_user=payload.to_user_id,
        content=payload.content,
        media_url=payload.media_url,
    )
    return msg


@router.get("/chat/conversations")
async def list_conversations(
    pagination: dict = Depends(pagination_params()),
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    pipeline = [
        {"$match": {"$or": [
            {"from_user_id": user_id},
            {"to_user_id": user_id}
        ]}},
        {"$project": {
            "other_id": {
                "$cond": [
                    {"$eq": ["$from_user_id", user_id]},
                    "$to_user_id",
                    "$from_user_id"
                ]
            },
            "created_at": 1
        }},
        {"$group": {
            "_id": "$other_id",
            "last_msg_at": {"$max": "$created_at"}
        }},
        {"$sort": {"last_msg_at": -1}},
        {"$skip": pagination["skip"]},
        {"$limit": pagination["limit"]},
    ]
    cursor = db[Message.collection_name].aggregate(pipeline)
    convos = await cursor.to_list(length=pagination["limit"])
    result = [
        {"user_id": str(c["_id"]), "last_message_at": c["last_msg_at"]} for c in convos
    ]
    return {"success": True, "data": {"conversations": result}}


@router.get("/chat/messages/{other_user_id}")
async def get_messages(
    other_user_id: str,
    pagination: dict = Depends(pagination_params()),
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    msgs = await Message.get_conversation(
        db,
        user_a=user_id,
        user_b=other_user_id,
        skip=pagination["skip"],
        limit=pagination["limit"],
    )
    return {"success": True, "data": {"messages": msgs}}
