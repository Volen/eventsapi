from fastapi import HTTPException, status
from deta import Deta
from schemas import PollBase, UserBase
from datetime import datetime


def create_poll(deta: Deta, request: PollBase, current_user: UserBase):
    polls_table = deta.Base('polls')

    check_active = polls_table.fetch({"is_active": True})
    if check_active.count < 1:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        new_poll = polls_table.put({
            "first_phase_minutes": request.first_phase_minutes,
            "second_phase_minutes": request.second_phase_minutes,
            "is_active": request.is_active,
            "activate_by_username": current_user['username'],
            "activate_by_userkey": current_user['key'],
            "start_time": current_time,
        })
        return new_poll
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Some poll is already active')


def active_poll(deta: Deta):
    polls_table = deta.Base('polls')
    check_active = polls_table.fetch({"is_active": True})
    if check_active.count < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no active poll')
    else:
        return check_active.items[0]
