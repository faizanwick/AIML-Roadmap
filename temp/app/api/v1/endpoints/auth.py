from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.repositories.user_repo import UserRespository
from app.services.auth_service import AuthService
from app.schemas.user_schemas import UserCreate, UserResponse, TokenResponse, LoginRequest
from app.models.user import User
from app.cores.security import decode_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

bearer_scheme = HTTPBearer()

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme), db : Session = Depends(get_db)):
    token = credentials.credentials
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_auth_service(db : Session = Depends(get_db)):
    repository = UserRespository(db)
    return AuthService(repository)

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user : UserCreate, service : AuthService = Depends(get_auth_service)):
    return service.register(user)

@router.post("/login", response_model=TokenResponse)
def login(credentials : LoginRequest, service : AuthService = Depends(get_auth_service)):
    return service.login(credentials.email, credentials.password)

@router.get("/me", response_model=UserResponse)
def get_me(current_user : User = Depends(get_current_user)):
    return current_user