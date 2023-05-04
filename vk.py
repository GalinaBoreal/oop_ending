import os
import requests
from dotenv import load_dotenv

load_dotenv()


class VK:

    def __init__(self, album_id, user_id, count=5, version='5.131'):
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.id = user_id
        self.album = album_id.lower()
        self.count = count
        self.version = version
        self.params = {'access_token': self.access_token, 'v': self.version}

    def users_info(self):
        """
        Получает в ВК информацию о пользователе методом get.
        :param: user_id, params
        :return: response.json()
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url=url, params={**self.params, **params})
        if response.status_code != 200:
            exit(f'Ошибка VK {response.status_code}')
        if 'error' in response.json():
            exit(f'Неверный токен VK')
        if not response.json()['response']:
            exit(f'ID не существует')

    def get_photo_data(self):
        """
        Запрашивает данные для загрузки фотографий методом photos.get
        :param: album_id, user_id, count, params
        :return: response.json()
        """
        self.users_info()
        url = "https://api.vk.com/method/photos.get"
        params = {
            'owner_id': self.id,
            'album_id': self.album,
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            'count': self.count
        }
        response = requests.get(url=url, params={**self.params, **params})
        if response.status_code != 200:
            exit(f'Ошибка VK {response.status_code}')
        else:
            return self.get_correct_photos(response.json())

    def get_correct_photos(self, data):
        """
        Выбирает наибольшие фотографии ВК.
        Создает словарь с данными для загрузки фото.
        :return: photos.
        """
        photos = {}
        if 'error' in data:
            exit(f'У пользователя закрытый профиль или неверно введен альбом')
        if not data['response']['items']:
            exit(f'У пользователя нет фотографий')
        for item in data['response']['items']:
            max_size = sorted(item['sizes'], key=lambda x: (x['width'], x['height']))[-1]
            url = max_size['url']
            size = max_size['type']
            likes_count = str(item['likes']['count'])
            if likes_count in photos:
                date = str(item['date'])
                likes_count = likes_count + '_' + date
            photos[likes_count] = {'url': url, 'size': size}
        return photos





