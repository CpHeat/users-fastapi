from datetime import datetime
from typing import List

from pydantic import BaseModel

from filtered_users import load_filtered_users


class User(BaseModel):
    """
    A user's details.

    :param login: The username of the user.
    :param login: The username of the user.
    :param login: The username of the user.
    """
    id: int
    login: str
    created_at: datetime
    avatar_url: str
    bio: str

class UserSummary(BaseModel):
    id: int
    login: str

raw_users = load_filtered_users("data/filtered_users.json")
users: List[User] = []

for user in raw_users:
    if isinstance(user.get("created_at"), str):
        user["created_at"] = user["created_at"].replace("Z", "+00:00")
        user["created_at"] = datetime.fromisoformat(user["created_at"])
    users.append(User(**user))