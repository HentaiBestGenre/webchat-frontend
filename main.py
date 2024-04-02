from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webchat.core.events import create_start_app_handler, create_stop_app_handler
from webchat.routes.api import router as api_router
from webchat.core.config import API_PREFXI, ALLOWED_HOSTS, HOST, PORT


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application),
    )

    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    application.include_router(api_router)

    return application


app = get_application()


if __name__ == "__mian__": 
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)