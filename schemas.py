from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserDisplay(BaseModel):
    key: str
    username: str


class PollBase(BaseModel):
    first_phase_minutes: int
    second_phase_minutes: int
    is_active: bool


class PollDisplay(BaseModel):
    key: str
    first_phase_minutes: int
    second_phase_minutes: int
    is_active: bool
    activate_by_username: str
    activate_by_userkey: str
    start_time: str


class FirstPhaseBase(BaseModel):
  poll_key: str
  username: str
  time: str
  event: str