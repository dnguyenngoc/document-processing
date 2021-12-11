
from fastapi import FastAPI
from settings import config
import uvicorn
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi.middleware.cors import CORSMiddleware
from databases.db_connect import Session
from starlette.requests import Request
from api.routes import v1
import time
import json


# ++++++++++++++++++++++++++++++++++++++++++++ DEFINE APP +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")

# ++++++++++++++++++++++++++++++++++++++++++++ HANDLE LOG FILE +++++++++++++++++++++++++++++++++++++++++++++++++++++++
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('logs/{}-{}-{}_{}h-00p-00.log'.format(
    config.u.year, config.u.month, config.u.day , config.u.hour), when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# ++++++++++++++++++++++++++++++++++++++++++++ ROUTER CONFIG ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app.include_router(v1.router, prefix="/api/v1")


# ++++++++++++++++++++++++++++++++++++++++++++ CORS MIDDLEWARE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ++++++++++++++++++++++++++++++++++++++++++++++ DB CONFIG ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response

# ++++++++++++++++++++++++++++++++++++++++++++++ RUN SERVICE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0',port=config.PORT,debug=True)