from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from webchat.db.repository import Repo
from webchat.dependencies import get_repository, get_session, get_manager
from webchat.models import (
    SendMessage,
    DeleteMessageModel,
    UpdateMessageModel
)


router = APIRouter()


@router.post("")
async def messages(
    message: SendMessage,
    session: AsyncSession = Depends(get_session),
    repository: Repo= Depends(get_repository),
    manager: Repo= Depends(get_manager)
):
    user = await repository.get_user(session, message.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    message = await repository.add_messages(
        session, 
        user_id = message.user_id,
        content = message.content,
        user_name = user.username
    )
    await manager.broadcast("create", message.to_dict())
    return message.to_dict()


@router.delete("/{message_id}")
async def messages(
    message_id: int, 
    data: DeleteMessageModel,
    session: AsyncSession = Depends(get_session),
    repository: Repo= Depends(get_repository),
    manager: Repo= Depends(get_manager)
):
    
    await repository.delete_message(session, message_id)
    messages = await repository.get_messages(session)
    messages = [i._asdict()['Message'].to_dict() for i in messages]
    await manager.broadcast("destroy", messages)
    return {}


@router.patch("/{message_id}")
async def messages(
    message_id: int, 
    data: UpdateMessageModel,
    session: AsyncSession = Depends(get_session),
    repository: Repo= Depends(get_repository),
    manager: Repo= Depends(get_manager)
):
    await repository.update_message(session, message_id, data.content)
    messages = await repository.get_messages(session)
    messages = [i._asdict()['Message'].to_dict() for i in messages]
    await manager.broadcast("update", messages)
    return {}
