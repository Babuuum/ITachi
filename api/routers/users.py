from typing import List

from fastapi import APIRouter, HTTPException, status

from core.services.user_db_services import UserDbServices
from api.schemas.user import UserResponse, UserUpdate
from core.db.session import SessionDep

router = APIRouter(prefix='/users', tags=['users'])

#soft_delete
#hard_del
#get
#get_all
#get_user_users
#update_user_users

@router.get('/', response_model=List[UserResponse])
async def get_users(session: SessionDep):
    users_list =  await UserDbServices.get_all_users(session)

    return users_list

@router.get('/by-name/{username}', response_model=UserResponse)
async def get_user_by_name(username: str, session: SessionDep):
    user =  await UserDbServices.get_user_by_name(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return user

@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, session: SessionDep):
    user =  await UserDbServices.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return user

@router.put('/{user_id}',response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    updated_user = await UserDbServices.update_user(session, user_id, user)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )

    return updated_user

@router.delete('/{user_id}')
async def delete_user(user_id: int, session: SessionDep):
    user_status =  await UserDbServices.delete_user(session, user_id)

    if not user_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return {"status": "success", "message": "user marked as inactive"}

@router.delete('/hard/{user_id}')
async def delete_user_hard(user_id: int, session: SessionDep):
    user_status =  await UserDbServices.delete_user_hard(session, user_id)

    if not user_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return {"status": "success", "message": "User_id deleted"}




