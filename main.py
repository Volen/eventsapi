from datetime import date, datetime, time, timedelta
from fastapi import FastAPI, WebSocket
from router import user, poll, first_phase
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from asyncio import sleep
from db.database import get_deta
from deta import Deta


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8081",
    "https://eventsfront.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(poll.router)
app.include_router(first_phase.router)


@app.websocket("/first_phase")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            deta: Deta = get_deta()
            polls_table = deta.Base('polls')
            active_poll = polls_table.fetch({"is_active": True}).items[0]
            first_phase_minutes = active_poll['first_phase_minutes']
            start_time = active_poll['start_time']
            start_hours, start_minutes, start_seconds = start_time.split(':')
            start_hours = int(start_hours)
            start_minutes = int(start_minutes)
            start_seconds = int(start_seconds)
            end_time = datetime.combine(date.today(), time(
            start_hours, start_minutes, start_seconds)) + timedelta(minutes=first_phase_minutes)
            first_phase_table = deta.Base('first_phase')
            first_phase_items = first_phase_table.fetch({"poll_key": active_poll['key']}).items

            await sleep(1)
            # Нужно выводить оставшееся время первой фазы и проголосовавших пользователей.
            resp = {
                'endtime': end_time.strftime("%H:%M:%S"),
                'first_phase_items': first_phase_items,
            }
            await websocket.send_json(resp)
        except Exception as error:
            print('error:', error)
            break
