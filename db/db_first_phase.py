from fastapi import HTTPException, status
from deta import Deta
from schemas import FirstPhaseBase, UserBase
from datetime import datetime


def create_first_phase(deta: Deta, request: FirstPhaseBase, current_user: UserBase):
    first_phase_table = deta.Base('first_phase')
    polls_table = deta.Base('polls')
    check_active = polls_table.fetch({"is_active": True})
    if check_active.count == 1:
        new_first_phase = first_phase_table.put({
            "poll_key": check_active.items[0]['key'],
            "username": current_user['username'],
            "userkey": current_user['key'],
            "time": request.time,
            "event": request.event,
        })
        return new_first_phase
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Нет активных голосований!')
