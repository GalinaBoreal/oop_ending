import requests
import yadisk
import wget
import json
import os
from datetime import datetime
from tqdm import tqdm


class VK:

    def __init__(self, ja_token, album_id, user_id, count=5, version='5.131'):
        self.access_token = "vk1.a.puVHDA5Y3YK8xSN383DaNHdHbGswjNWq6qvTGlk0T4K0ZT3T" \
                            "-zpi6H5dIy4PtmTPOCm8Q9dVNhJO34MXfqikTtFqWefxoMnz2oeBrQpn9UAr" \
                            "-m7vPblRtlmPRbTFKdOLBkY3TaFWnLF9OpSUr_BxDyxAyYew7soi_uhU2YGe" \
                            "-NqUHm4c4O8X9HOXl0Ds8E90NHDdFsC_r0eOpcXuKVfOwA"
        self.ya_token = ya_token
        self.id = user_id
        self.album = album_id
        self.count = count
        self.version = version
        self.params = {'access_token': self.access_token, 'v': self.version}
        self.get_photo_data = {}
        self.photo_name_list = []
        self.persona_name = []

    def _users_info(self):
        """
        Получение информации о пользователе
        param: user_id
        param: params
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url=url, params={**self.params, **params})
        if response.status_code == 200:
            response = response.json()
            if response['response'] != []:
                self.persona_name.append(response['response'][0]['first_name'])
                self.persona_name.append(response['response'][0]['last_name'])
        else:
            return 'Что то пошло не так при получении информации о профиле VK.'
        return

    def _get_photo_data(self):
        """
        Запросить данные для загрузки фотографий методом photos.get,
        получить итоговые данные в формате json,
        param: album_id
        param: count
        param: params
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
        if response.status_code == 200:
            response = response.json()
            self.get_photo_data.update(response)
            return self.get_photo_data
        else:
            return 'Что то пошло не так при получении информации о фотографиях VK.'

    def _download_photo(self):
        """
        Загружает фото в локальную папку Photos,
        присвоив файлу имя = количество лайков или
        дата+количество лайков, если лайков одинаковое
        количество.
        Запись результата загрузки в файл photos.json
        params: self._get_photo_data
        """

        photo_list = []
        type_list = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']

        for item in self.get_photo_data['response']['items']:
            flag = False
            photo_name = str(item['likes']['count']) + '.jpg'
            if photo_name not in self.photo_name_list:
                self.photo_name_list.append(photo_name)
            else:
                photo_name = str(item['date']) + photo_name
                self.photo_name_list.append(photo_name)
            for type in type_list:
                for dict in item['sizes']:
                    if dict['type'] == type and flag == False:
                        flag = True
                        url = dict['url']
                        size = dict['type']
                        wget.download(url=url, out='Photos/' + photo_name)
                        photo_list.append({'file_name': photo_name, 'size': size})

        with open('photos.json', 'w') as outfile:
            json.dump(photo_list, outfile)

        return self.photo_name_list

    def _upload_poto_yd(self):
        """
        Вызывает self._download_photo() для загрузки файлов в Photos.
        Создает папку с текущей датой на яндекс диске
        и, используя библиотеку-клиент REST API Яндекс.Диска jadisk,
        загружает в нее фотографии из локальной папки Photos,
        param: self._download_photo()
        param: ya_token
        param: name_list
        """
        y = yadisk.YaDisk(token=self.ya_token)
        flag = y.check_token()
        date = str(datetime.now().date())
        dir = 'Photo_VK_' + date
        if flag == False:
            print("Неверный токен яндекс диска.")
        else:
            try:
                y.mkdir(dir)
                for i in tqdm(range(len(self.photo_name_list))):
                    name = self.photo_name_list[i]
                    y.upload(f'Photos/{name}', f'{dir}/{name}')
                print(
                    f'Фотографии {self.album} пользователя {" ".join(self.persona_name)} загружены на яндекс диск '
                    f'успешно.')
            except Exception:
                print('Что то пошло не так во время загрузки фотографий на яндекс диск.')
        return

    def check_profile(self):
        """
        Проверка профиля пользователя по ключевым моментам:
        существует ли Id, не закрыт ли профиль, есть ли фото.
        Если исключений нет, вызывает метод self._upload_poto_yd()
        для загрузки и выгрузки файлов и создания итогового файла photos.json
        """
        self._users_info()
        if self.persona_name == []:
            return 'Id не существует.'
        else:
            self._get_photo_data()
            if 'error' in self.get_photo_data:
                return f'Профиль пользователя {" ".join(self.persona_name)} закрыт, либо неверно введен альбом.'
            else:
                if self.get_photo_data['response']['items'] == []:
                    return f'У пользователя {" ".join(self.persona_name)} нет фотографий.'
                else:
                    self._download_photo()
                    print(f'\nФотографии {self.album} пользователя {" ".join(self.persona_name)} скопированы с VK '
                          f'успешно.\nЗагружаем на яндекс диск...')
                    self._upload_poto_yd()
                    for name in self.photo_name_list:
                        path = "Photos/" + name
                        os.remove(path)
                    return '\nПрограмма завершена!'


ya_token = str(input('Введите токен яндекс диска: '))
album_id = str(input('Для выбора альбома введите profile или wall: '))
album_id = album_id.lower()
user_id = str(input('Введите id пользователя VK: '))

vk = VK(ya_token, album_id, user_id)
print(vk.check_profile())
