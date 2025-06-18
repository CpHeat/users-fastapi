import json
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv()

security = HTTPBasic()


authorized_users_json = os.getenv("AUTHORIZED_USERS", "[]")
authorized_users = json.loads(authorized_users_json)

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Handles the authentication.

    :param credentials: A login/password combination.
    :type credentials: HTTPBasicCredentials

    :return: The authenticated user username.
    """
    for authorized_user in authorized_users:
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = f"{authorized_user['login']}".encode('utf-8')
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = f"{authorized_user['password']}".encode('utf-8')
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )
        if is_correct_username and is_correct_password:
            return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"}
    )