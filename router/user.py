from typing import List
from schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from deta import Deta
from db.database import get_deta
from db import db_user
from auth.oauth2 import get_current_user


router = APIRouter(
  prefix='/user',
  tags=['user']
)

# Create user
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, deta: Deta = Depends(get_deta)):
  return db_user.create_user(deta, request)

# Read all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
  return db_user.get_all_users(deta)

# Read one user
@router.get('/{key}', response_model=UserDisplay)
def get_user(key: str, deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
  return db_user.get_user(deta, key)

# Update user
@router.post('/{key}/update')
def update_user(key: str, request: UserBase, deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
  return db_user.update_user(deta, key, request)

# Delete user
@router.get('/delete/{key}')
def delete(key: str, deta: Deta = Depends(get_deta), current_user: UserBase = Depends(get_current_user)):
  return db_user.delete_user(deta, key)

# For testing
@router.get("/test/me", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return current_user