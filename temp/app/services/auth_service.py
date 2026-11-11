from fastapi import HTTPException
from app.repositories.user_repo import UserRespository
from app.schemas.user_schemas import UserCreate, UserResponse
from app.cores.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, repository : UserRespository):
        self.repository = repository

    def register(self, user : UserCreate) -> UserResponse:
        existing_user = self.repository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(status_code=409, detail="User Already Exist")

        user_data = user.model_dump(exclude={"password"})
        user_data["hashed_password"] = hash_password(user.password)

        new_user = self.repository.create(user_data)
        return UserResponse.model_validate(new_user)

    def login(self, email : str, password : str):
        user = self.repository.get_by_email(email)

        if not user or not user.hashed_password:
            raise HTTPException(status_code=401, detail="Invalid Email or Password", headers={"WWW-Authenticate" : "Bearer"})

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid Email or Password", headers={"WWW-Authenticate" : "Bearer"})

        access_token = create_access_token(user.user_id)

        return {"access_token" : access_token, "token_type" : "bearer"}