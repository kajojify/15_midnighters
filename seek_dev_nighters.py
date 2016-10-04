import requests
from datetime import datetime, time


def load_attempts():
    """Загружает информацию с devman о том, кто и когда отправил задачу
    на проверку, в виде json. Возвращает объект-генератор, на каждой итерации
    генерирующий словарь, содержащий ник отправившего задачу, его временную
    зону и количество секунд прошедшее с 00:00:00 UTC 1 января, 1970 года."""

    url = "https://devman.org/api/challenges/solution_attempts/"
    devman_response = requests.get(url, params={'page': 1})
    devman_data = devman_response.json()
    pages = devman_data['number_of_pages']
    for page_number in range(1, pages+1):
        payload = {'page': page_number}
        devman_response = requests.get(url, params=payload)
        devman_data = devman_response.json()
        users = len(devman_data['records'])
        for user_number in range(0, users):
            yield {
                'username': devman_data['records'][user_number]['username'],
                'timestamp': devman_data['records'][user_number]['timestamp'],
                'timezone': devman_data['records'][user_number]['timezone'],
            }


def get_midnighters(users):
    """Среди пользователей devman отбирает тех, кто отправлял задачи в
    промежуток от 00:00 до 04:00. Возвращает список, элементами которого
     являются ники "пользователей-сов". """

    midnight_users_list = []
    for user in users:
        user_datetime = datetime.fromtimestamp(user['timestamp'])
        # user_datetime содержит время уже относительно часовой зоны юзера,
        # так как timestamp имеет значение относительно часовой зоны юзера
        user_time = user_datetime.time()
        if time(0, 0, 0) < user_time < time(4, 0, 0):
            if user['username'] not in midnight_users_list:
                midnight_users_list.append(user['username'])
    return midnight_users_list

if __name__ == '__main__':
    users_list = list(load_attempts())
    midnight_users_list = get_midnighters(users_list)
    print("Совы devman, отправялющие задачи в промежуток 00:00 - 04:00:\n")
    for user in midnight_users_list:
        print(user)
