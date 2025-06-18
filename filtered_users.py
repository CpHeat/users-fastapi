import json
from datetime import datetime

import pandas as pd


def remove_duplicates(users_list:list[dict]) -> list[dict]:
    """
    Removes duplicates from a users list.

    :param users_list: The users list.
    :type users_list: list[dict]

    :return: The unique users list.
    """
    df = pd.DataFrame(users_list)
    df_unique = df.drop_duplicates(subset="id")
    print(f"Duplicates removed: {len(df) - len(df_unique)}")
    return df_unique.to_dict(orient="records")

def filter_users(required_fields:tuple[str, ...], creation_date_filter:str, users_list:list[dict]) -> list[dict]:
    """
    Applies filters to a users list.

    :param needed_fields: The required fields.
    :type users_list: tuple[str]
    :param creation_date_filter: The oldest acceptable creation date.
    :type creation_date_filter: str
    :param users_list: The users list.
    :type users_list: list[dict]

    :return: The filtered users list.
    """
    filtered_users = []
    df = pd.DataFrame(users_list)

    for field in required_fields:
        if field in df.columns:
            df = df[df[field].notna() & (df[field] != "")]
        else:
            return []

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
        creation_limit = pd.to_datetime(creation_date_filter).tz_localize("UTC")
        df = df[df["created_at"] >= creation_limit]
        df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"Filtered out users: {len(users_list) - len(df)}")
    return df.to_dict(orient="records")

def load_users(file:str):
    """
    Loads a users information list from a JSON file.

    :param file: The JSON file to get the users list from.
    :type file: str

    :return: The users list.
    """
    users = json.load(open(file))
    print(f"Loaded users: {len(users)}")
    return users

def save_filtered_users(users_list:list[dict]):
    """
    Saves the filtered users information list in a JSON file.

    :param users_list: A list of users information.
    """
    with open('data/filtered_users.json', 'w') as fp:
        json.dump(users_list, fp, indent=4)
    print(f"Saved filtered users: {len(users_list)}")

def load_filtered_users(file_path:str):
    """
    Loads a filtered users information list from a JSON file.

    :param file_path: The path to the JSON file to get the users list from.
    :type file_path: str

    :return: The users list.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        users = json.load(f)
        print(f"Loaded users: {len(users)}")
        return users