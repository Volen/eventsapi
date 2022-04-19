from datetime import datetime
from asyncio import sleep
from schemas import FirstPhaseBase, PollBase, PollDisplay, UserBase
from fastapi import APIRouter, WebSocket, Depends
from deta import Deta
from db.database import get_deta
from db import db_first_phase
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/first_phase',
    tags=['first_phase']
)

@router.post('/', response_model=FirstPhaseBase)
def create_poll(request: FirstPhaseBase, deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
    return db_first_phase.create_first_phase(deta, request, current_user)

