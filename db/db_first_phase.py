from fastapi import HTTPException, status
from deta import Deta
from schemas import FirstPhaseBase, UserBase

def create_first_phase(deta: Deta, request: FirstPhaseBase, current_user: UserBase):
    first_phase_table = deta.Base('first_phase')
    polls_table = deta.Base('polls')
    check_active = polls_table.fetch({"is_active": True})
    if check_active.count == 1:

        check_already_vote = first_phase_table.fetch({"poll_key": check_active.items[0]['key'], "username": current_user['username'], "userkey": current_user['key']})            

        if check_already_vote.count == 0:
            new_first_phase = first_phase_table.put({
                "poll_key": check_active.items[0]['key'],
                "username": current_user['username'],
                "userkey": current_user['key'],
                "time": request.time,
                "event": request.event,
            })

            # Пополняем запас словаря мероприятий для автозаполнения поля ввода мероприятий            
            event_dict_table = deta.Base('event_dict')

            if event_dict_table.fetch({"event": request.event}).count == 0:
                event_dict_table.put({"event": request.event})

            return new_first_phase
        else:    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Вы уже голосовали!')

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Нет активных голосований!')
