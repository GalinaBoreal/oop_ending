import requests
from tqdm import tqdm
import json


class YD:

    def __init__(self, token):
        self.token = token

    def get_folder(self, ydisk_folder_path):
        """
        Создает папку на яндекс диске методом put.
        :param: ydisk_folder_path: расположение и имя папки
        :return: в случае ошибки - код ошибки
        """
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {"path": ydisk_folder_path}
        response = requests.put(url=url, headers=headers, params=params)
        if response.status_code not in (201, 409):
            exit(f'Ошибка YD {response.status_code}')

    def upload_photo(self, data, ydisk_folder_path="Photos_vk"):
        """
        Вызывает get_folder(), имя папки: Photos_vk.
        Загружает файл на яндекс диск методом post,
        используя данные метода VK.get_correct_photos().
        Процесс загрузки сопровождается прогресс баром tqdm.
        Формирует файл photos.json.
        :param: params содержит расположение и имя файла и ссылку на файл
        :return: в случае ошибки - код ошибки
        """
        self.get_folder(ydisk_folder_path)
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        json_list = []
        for key, value in tqdm(data.items()):
            url = value['url']
            file_name = key + '.jpg'
            path = ydisk_folder_path + '/' + file_name
            params = {"path": path, 'url': url}
            response = requests.post(url=upload_url, headers=headers, params=params)
            if response.status_code != 202:
                exit(f'Ошибка YD {response.status_code}')
            json_list.append({'file_name': file_name, 'size': value['size']})
        with open('photos.json', 'w') as outfile:
            json.dump(json_list, outfile)

        return f'Фотографии загружены на яндекс диск успешно!'
