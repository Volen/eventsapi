from datetime import datetime
from asyncio import sleep
from schemas import PollBase, PollDisplay, UserBase
from fastapi import APIRouter, WebSocket, Depends
from deta import Deta
from db.database import get_deta
from db import db_poll
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/poll',
    tags=['poll']
)

# Create poll
@router.post('/', response_model=PollBase)
def create_poll(request: PollBase, deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
    return db_poll.create_poll(deta, request, current_user)

# Get active poll
@router.get('/active', response_model=PollDisplay)
def get_active_poll(deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
    return db_poll.active_poll(deta)

