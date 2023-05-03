import json
import os
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from yd import YD


class VK:

    def __init__(self, access_token, album_id, user_id, count=5, version='5.131'):
        self.access_token = access_token
        self.id = user_id
        self.album = album_id
        self.count = count
        self.version = version
        self.params = {'access_token': self.access_token, 'v': self.version}

    def _users_info(self):
        """
        Получает в ВК информацию о пользователе методом get.
        :param: user_id, params
        :return: response.json() или сообщение об ошибке и завершение программы
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url=url, params={**self.params, **params})
        if response.status_code < 200 and response.status_code > 300:
            print(f'Ответ VK: ошибка {response.status_code}')
            return exit(0)
        else:
            return response.json()

    def _get_photo_data(self):
        """
        Запрашивает данные для загрузки фотографий методом photos.get
        :param: album_id, user_id, count, params
        :return: response.json() или сообщение об ошибке и завершение программы
        """
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
        if response.status_code < 200 and response.status_code > 300:
            print(f'Ответ VK: ошибка {response.status_code}')
            return exit(0)
        else:
            return response.json()

    def _get_photo_url(self):
        """
        Вызывает метод _get_photo_data() и обрабатывает ответ,
        выбирая наибольшие фотографии ВК. Имена фотографий = количество лайков
        или дата + количество лайков, если лайков одинаковое количество.
        Формирует файл photos.json.
        :return: словарь name_url, ключ - имя файла, значение - ссылка для загрузки.
        """
        json_list = []
        name_url = {}
        type_list = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        data = self._get_photo_data()
        for item in data['response']['items']:
            flag = False
            photo_name = str(item['likes']['count']) + '.jpg'
            if photo_name not in name_url:
                name_url[photo_name] = None
            else:
                photo_name = str(item['date']) + photo_name
                name_url[photo_name] = None
            for type in type_list:
                for dict in item['sizes']:
                    if dict['type'] == type and flag == False:
                        flag = True
                        url = dict['url']
                        size = dict['type']
                        name_url[photo_name] = [url]
                        json_list.append({'file_name': photo_name, 'size': size})

        with open('photos.json', 'w') as outfile:
            json.dump(json_list, outfile)

        return name_url

    def uploader(self):
        """
        Загрузка фотографий на яндекс диск.
        Проверяет ID пользователя: не существует, закрыт, нет фото - выводит сообщение.
        Вызывает self._users_info() для получения информации о пользователе.
        Вызывает self._get_photo_url() для получения данных для загрузки.
        Вызывает класс YD: yd.get_folder() для создания папки,
        имя папки: Photo_VK_ + user_id; yd.get_upload_link() для загрузки
        файлов, процесс загрузки сопровождается прогресс баром tqdm.
        :return: Завершение программы
        """
        info = self._users_info()
        if info['response'] == []:
            return f'ID не существует.'
        else:
            data = self._get_photo_data()
            if 'error' in data:
                return f'У пользователя {info["response"][0]["first_name"]} \
{info["response"][0]["last_name"]} закрытый профиль.'
            else:
                if data['response']['items'] == []:
                    return f'У пользователя {info["response"][0]["first_name"]} \
{info["response"][0]["last_name"]} нет фотографий'
                else:
                    dict = self._get_photo_url()
                    dir = 'Photo_VK_' + str(self.id) + '/'
                    yd.get_folder(ydisk_folder_path=dir)
                    for key in tqdm(dict.keys()):
                        path = dir + str(key)
                        yd.get_upload_link(path, dict[key])
        return f'Фотографии {self.album} пользователя {info["response"][0]["first_name"]} \
{info["response"][0]["last_name"]} загружены на яндекс диск успешно!'


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

ya_token = str(input('Введите токен яндекс диска: '))
album_id = str(input('Для выбора альбома введите profile или wall: '))
album_id = album_id.lower()
user_id = str(input('Введите id пользователя VK: '))

yd = YD(token=ya_token)
vk = VK(access_token, album_id, user_id)
print(vk.uploader())
