from deta import Deta
from fastapi import HTTPException, status
from db.hash import Hash
from schemas import UserBase

def create_user(deta: Deta, request: UserBase):
  users_table = deta.Base('users')
  new_user = users_table.put({
    "username": request.username,
    "password": Hash.bcrypt(request.password)
  })
  return new_user

def get_all_users(deta: Deta):
  users_table = deta.Base('users')
  return users_table.fetch().items

def get_user(deta: Deta, key: str):
  users_table = deta.Base('users')
  user = users_table.get(key)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with key {key} not found')
  return user  

def get_user_by_username(deta: Deta, username: str):
  users_table = deta.Base('users')
  user = users_table.fetch({"username": username}).items

  if len(user) < 1:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

  user = user[0]    

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
  return user  

def update_user(deta: Deta, key: str, request: UserBase):
  users_table = deta.Base('users')
  user = users_table.get(key)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with key {key} not found')
  updates = {
    "username": request.username,
    "password": Hash.bcrypt(request.password)
  }
  users_table.update(updates, key)
  return 'ok'

def delete_user(deta: Deta, key: str):
  users_table = deta.Base('users')
  user = users_table.get(key)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with key {key} not found')
  users_table.delete(key)
  return 'ok'