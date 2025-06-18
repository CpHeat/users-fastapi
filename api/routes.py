from typing import List

from fastapi import APIRouter, Query, HTTPException, Depends

from api.models import UserSummary, User, users
from api.security import authenticate

router = APIRouter()


@router.get("/users/", response_model=List[UserSummary])
def get_users(skip:int = Query(0, ge=0), limit: int = Query(None, ge=1), username: str = Depends(authenticate)) -> list[UserSummary]:
    """
    Returns a list of users.

    Authentication required:
    - **Pass HTTP Basic credentials in the `Authorization` header.**

    - **skip**: How many users to skip (optional - default = 0).
    - **limit**: How many users to return (optional - minimum = 1).
    """
    if limit is None:
        selected_users = users[skip:]
    else:
        selected_users = users[skip:skip + limit]
    return [UserSummary(id = u.id, login=u.login) for u in selected_users]

@router.get("/users/search", response_model=List[UserSummary])
def search_users(q: str = Query(..., min_length=1), username: str = Depends(authenticate)) -> list[UserSummary] | str:
    """
    Returns a list of users whose login contains the specified string.

    Authentication required:
    - **Pass HTTP Basic credentials in the `Authorization` header.**

    - **q**: The string to search for.
    - **username**: An authenticated user's username.
    """
    found_users = []
    for u in users:
        if q.lower() in u.login.lower():
            found_users.append(u)
    return [UserSummary(id = u.id, login=u.login) for u in found_users]

@router.get("/users/{user_login}")
def get_user(user_login: str, username: str = Depends(authenticate)) -> User:
    """
    Returns details about a specific user.

    Authentication required:
    - **Pass HTTP Basic credentials in the `Authorization` header.**

    - **user_login**: The login to search for.
    - **username**: An authenticated user's username.
    """
    for u in users:
        if u.login == user_login:
            return u
    raise HTTPException(status_code=404, detail="User not found")