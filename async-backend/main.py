from fastapi import FastAPI

from server.handlers import on_startup
from settings import ALLOWED_HOSTS, ALLOWED_METHODS, DEBUG

from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="AI", docs_url="/ai/docs/", redoc_url="/ai/redoc/", debug=DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=["*"],
)


app.add_event_handler("startup", on_startup(app))
