from fastapi import APIRouter
from api.resources.v1 import account, demo
from api.resources.v1.ml_process import ml_main


router_v1 = APIRouter()


router_v1.include_router(demo.router, prefix="/demo",  tags=["V1-demo"])
router_v1.include_router(account.router, prefix="/account",  tags=["V1-Account"])
router_v1.include_router(ml_main.router, prefix="/ml",  tags=["V1-ML"])

