from asyncio import sleep
from schemas import EventDictBase, UserBase
from fastapi import APIRouter, WebSocket, Depends
from deta import Deta
from db.database import get_deta
from db import db_event_dict
from auth.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/event_dict',
    tags=['event_dict']
)

@router.get('/', response_model=List[EventDictBase])
def get_all_events(deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
    return db_event_dict.get_all_events_words(deta)