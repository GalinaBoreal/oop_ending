import json
import os
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from yd import YD

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
        return response.json()

    def get_photo_data(self):
        """
        Вызывает self._users_info() для проверки ID пользователя.
        Запрашивает данные для загрузки фотографий методом photos.get
        :param: album_id, user_id, count, params
        :return: response.json()
        """
        check_user = self.users_info()
        if not check_user['response']:
            exit(f'ID не существует')
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
            return response.json()

    def get_correct_photos(self):
        """
        Вызывает метод _get_photo_data(), проверяет профиль пользователя.
        Обрабатывает ответ, выбирая наибольшие фотографии ВК.
        Создает словарь с данными для загрузки фото.
        :return: photos.
        """
        photos = {}
        data = self.get_photo_data()
        if 'error' in data or data['response']['items'] == []:
            exit(f'У пользователя закрытый профиль или нет фотографий')
        for item in data['response']['items']:
            max_size = sorted(item['sizes'], key=lambda x: (x['width'], x['height']))[-1]
            url = max_size['url']
            size = max_size['type']
            likes_count = str(item['likes']['count']) + '.jpg'
            if likes_count in photos:
                date = str(item['date'])
                likes_count = date + '_' + likes_count
            photos[likes_count] = {'url': url, 'size': size}
        return photos

    def uploader(self):
        """
        Загрузка фотографий на яндекс диск.
        Вызывает self._get_photo_url() для получения данных для загрузки.
        Вызывает класс YD: yd.get_folder() для создания папки,
        yd.upload_photo() для загрузки файлов в папку.
        Процесс загрузки сопровождается прогресс баром tqdm.
        Формирует файл photos.json.
        :return: Завершение программы
        """
        photos = self.get_correct_photos()
        json_list = []
        folder = 'Photo_VK_' + str(self.id) + '/'
        yd.get_folder(folder)
        for key in tqdm(photos.keys()):
            path = folder + str(key)
            yd.upload_photo(path, photos[key]['url'])
            json_list.append({'file_name': key, 'size': photos[key]['size']})
        with open('photos.json', 'w') as outfile:
            json.dump(json_list, outfile)
        return f'Фотографии загружены на яндекс диск успешно!'


ya_token = (input('Введите токен яндекс диска: '))
album_id = (input('Для выбора альбома введите profile или wall: '))
user_id = (input('Введите id пользователя VK: '))

yd = YD(token=ya_token)
vk = VK(album_id, user_id)
print(vk.uploader())
