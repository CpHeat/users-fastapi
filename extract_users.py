import datetime
import json
import os
import time

from dotenv import load_dotenv
import requests
from requests import get, Response
from requests.exceptions import Timeout, ConnectionError

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

def safe_get(session, url, headers, max_retries=3, timeout=10):
    for attempt in range(1, max_retries + 1):
        try:
            return session.get(url, headers=headers, timeout=timeout)
        except (ConnectionError, Timeout) as e:
            print(f"[{attempt}/{max_retries}] Erreur de connexion : {e}")
            time.sleep(5 * attempt)
    print("Échec de la connexion après plusieurs tentatives.")
    return None

def get_users_info(users_nb:int, since:int) -> list[dict]:
    """
    Gets a list of GitHub users with their information.

    :param users_nb: How many users to get.
    :type users_nb: int
    :param since: The id after which to get users.
    :type since: int

    :return: List of GitHub users with their information.
    """
    print("Getting users info...")
    failed_pages = 0
    failed_users = 0

    if users_nb <= 100:
        per_page = last_batch = users_nb
        iterations = 1
    else:
        per_page = 100
        iterations = users_nb // 100 + 1
        last_batch = users_nb % 100

    session = requests.Session()
    users_info = []
    i = 1

    while i <= iterations:
        if i == iterations:
            print(f"==================== Batch {i}: {last_batch} users, starting at id {since} ====================")
            url = f"https://api.github.com/users?per_page={last_batch}&since={since}"
        else:
            print(f"==================== Batch {i}: {per_page} users, starting at id {since} ====================")
            url = f"https://api.github.com/users?per_page={per_page}&since={since}"

        while True:
            result = safe_get(session, url, headers=headers)

            if result is None:
                print("Connection failed, retry...")
                session.close()
                session = requests.Session()
                continue

            #result = get(url, headers=headers)
            error_handling = handle_status_code(result)
            time.sleep(get_delay(result))

            if error_handling["error"]:
                if error_handling["end_script"]:
                    return users_info
                elif error_handling["pass"]:
                    i += 1
                    failed_pages += 1
                    continue
                else:
                    time.sleep(error_handling["timeout"])
                    continue

            json_result = json.loads(result.content)
            for idx, result in enumerate(json_result):
                user_detail = get_user_detail(result["login"], session)
                if user_detail.get("not_found"):
                    print("User not found")
                    failed_users += 1
                    continue
                if user_detail:
                    since = user_detail["id"]
                    users_info.append(user_detail)
                else:
                    print(f"Got informations about {len(users_info)} users. {failed_pages} failed pages and {failed_users} failed users.")
                    return users_info

            i += 1
            break

    print(f"Got informations about {len(users_info)} users. {failed_pages} failed pages and {failed_users} failed users.")
    return users_info

def get_user_detail(user_login:str, session: requests.Session) -> dict | None:
    """
    Gets the details of a GitHub user.

    :param user_login: The user's login.
    :type user_login: str
    :param session: The requests current session..
    :type session: requests.Session

    :return: The user's details.
    """
    print(f"Getting details for {user_login}")
    url = f"https://api.github.com/users/{user_login}"
    user_detail = None

    while True:
        print("new while")
        result = safe_get(session, url, headers=headers)

        if result is None:
            print("Connection failed for this user, retry...")
            session.close()
            session = requests.Session()
            continue

        #result = get(url, headers=headers)
        error_handling = handle_status_code(result)
        time.sleep(get_delay(result))

        if error_handling["error"]:
            print("error")
            if error_handling["end_script"]:
                print("end_script")
                return user_detail
            elif error_handling["pass"]:
                print("pass")
                return {"not_found": True}
            else:
                print("else")
                time.sleep(error_handling["timeout"])
                continue

        json_result = json.loads(result.content)
        user_detail = {
            "login": user_login,
            "id": json_result["id"],
            "created_at": json_result["created_at"],
            "avatar_url": json_result["avatar_url"],
        }

        if json_result["bio"]:
            user_detail["bio"] = json_result["bio"]

        return user_detail

def get_delay(response:Response) -> int:
    """
    Gets the delay in seconds before making another API call.

    :param response: The API response that contains quota information.
    :type response: requests.Response
    :return: The delay before continuing to make API Calls, in seconds.
    """
    try:
        remaining_calls = int(response.headers.get("X-RateLimit-Remaining"))
        reset_timestamp = int(response.headers.get("X-RateLimit-Reset"))
    except Exception as e:
        print("Headers without RateLimit data, defaulting to 60s sleep.", e)
        return 60

    print("remaining_calls", remaining_calls)
    if remaining_calls > 0:
        return 0
    else:
        delay = max(0, reset_timestamp - int(time.time()))
        resume_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        resume_time_str = resume_time.strftime("%H:%M:%S")
        print(f"==================== Quota reached, delaying calls for {delay} seconds (until {resume_time_str}) ====================")
        return delay

def handle_status_code(response:Response) -> dict:
    """
    Specifies how to handle request's status code.

    :param response: The API response that contains the status code.
    :return: How to handle the error through a dict
    """
    if response.status_code == 403:
        if response.headers.get("X-RateLimit-Reset"):
            print(f"Error: API call forbidden (quota issue)")
            delay = get_delay(response)
            return {
                "error": True,
                "end_script": False,
                "pass": False,
                "timeout": delay
            }
        else:
            print(f"Error: API call forbidden (token issue)")
            return {
                "error": True,
                "end_script": True,
                "pass": False,
                "timeout": 0
            }
    elif response.status_code== 5:
        print(f"Error: GitHub server is down, retry later.")
        return {
            "error": True,
            "end_script": False,
            "pass": False,
            "timeout": 60
        }
    elif response.status_code == 429:
        print(f"Error: Too many requests.")
        return {
            "error": True,
            "end_script": False,
            "pass": False,
            "timeout": 5
        }
    elif response.status_code == 404:
        print(f"Error: Page not found.")
        return {
            "error": True,
            "end_script": False,
            "pass": True,
            "timeout": 0
        }
    elif response.status_code != 200:
        print(f"Error: Unexpected response from GitHub: {response.status_code}")
        return {
            "error": True,
            "end_script": True,
            "pass": False,
            "timeout": 0
        }
    else:
        return {
            "error": False,
            "end_script": False,
            "pass": False,
            "timeout": 0
        }

def save_users(users_info:list[dict]) -> None:
    """
    Saves the users information list in a JSON file.

    :param users_info: A list of users information.
    """
    with open('data/users.json', 'w') as fp:
        json.dump(users_info, fp, indent=4)
    print(f"Saved {len(users_info)} users information")