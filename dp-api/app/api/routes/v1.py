from fastapi import APIRouter
from api.resources.v1 import (account)


router = APIRouter()


router.include_router(account.router, prefix="/account",  tags=["V1-Account"])
