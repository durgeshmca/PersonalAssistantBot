from fastapi import APIRouter,Body
from app.models.users import UserBase,create_user,UserCreate
from app.auth import (
    Annotated,
    Depends,
    get_current_active_user,
    get_password_hash
)
from app.lib.db import SessionDep
users_router = APIRouter()

@users_router.post("/users",response_model=UserBase,tags=["users"])
async def create_new_user(user: Annotated[UserCreate, Body()],
                          session:SessionDep):
   user.password = get_password_hash(user.password)
   user = create_user(session, user)
   return user

@users_router.get("/users/me/", 
            response_model=UserBase,
            tags=["users"]
        )
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
):
    return current_user



