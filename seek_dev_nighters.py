import requests
from pytz import timezone
from datetime import datetime, time


def load_attempts():
    url = "https://devman.org/api/challenges/solution_attempts/"
    first_page = 1
    users_list = []
    devman_response = requests.get(url, params={'page': first_page})
    devman_data = devman_response.json()
    pages = devman_data['number_of_pages']
    users = devman_data['records']
    for user in users:
            users_list.append({
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone'],
            })
    for page_number in range(first_page + 1, pages + 1):
        payload = {'page': page_number}
        devman_response = requests.get(url, params=payload)
        devman_data = devman_response.json()
        users = devman_data['records']
        for user in users:
            users_list.append({
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone'],
            })
        return users_list

def get_midnighters(users):
    midnight_users_list = []
    for user in users:
        if user['timestamp'] is None:
            continue
        server_time_zone = timezone("Europe/Moscow")
        server_datetime = datetime.fromtimestamp(user['timestamp'])
        server_datetime_localized = server_time_zone.localize(server_datetime)
        user_time_zone = timezone(user['timezone'])
        user_time = server_datetime_localized.astimezone(user_time_zone)
        if time(0, 0, 0) < user_time.time() < time(4, 0, 0):
            if user['username'] not in midnight_users_list:
                midnight_users_list.append(user['username'])
    return midnight_users_list


if __name__ == '__main__':
    users_list = load_attempts()
    midnight_users_list = get_midnighters(users_list)
    print("Совы devman, отправялющие задачи в промежуток 00:00 - 04:00:\n")
    for user in midnight_users_list:
        print(user)
