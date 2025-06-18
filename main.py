from extract_users import get_users_info, save_users
from filtered_users import load_users, remove_duplicates, filter_users, save_filtered_users


if __name__ == "__main__":

    # users_info = get_users_info(10000, 10361000)
    # save_users(users_info)

    users = load_users('data/users.json')
    unique_users = remove_duplicates(users)
    filtered_users = filter_users(("bio", "avatar_url"), "2015-01-01", unique_users)
    save_filtered_users(filtered_users)