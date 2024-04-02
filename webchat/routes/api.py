from fastapi import APIRouter

from webchat.routes import (
    auth, messages, websockets
)


router = APIRouter()

router.include_router(auth.router,          tags=["auth"],              prefix=""          )
router.include_router(messages.router,      tags=["messages"],          prefix="/messages"  )
router.include_router(websockets.router,    tags=["websockets"],        prefix="/ws"        )
