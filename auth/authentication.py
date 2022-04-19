import pprint
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from deta import Deta
from db.database import get_deta
from db.hash import Hash
from auth import oauth2

router = APIRouter(
  tags=['authentication']
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), deta: Deta = Depends(get_deta)):
  users_table = deta.Base('users')
  user = users_table.fetch({"username": request.username}).items
  
  if len(user) < 1:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

  user = user[0]

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
  if not Hash.verify(user['password'], request.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
  
  access_token = oauth2.create_access_token(data={'sub': user['username']})

  return {
    'access_token': access_token,
    'token_type': 'bearer',
    'user_key': user['key'],
    'username': user['username']
  }