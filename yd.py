import requests


class YD:

    def __init__(self, token):
        self.token = token

    def get_folder(self, ydisk_folder_path):
        """
        Создает папку на яндекс диске.
        :param ydisk_folder_path: расположение и имя папки
        :return: в случае ошибки - код ошибки
        """
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {"path": ydisk_folder_path}
        response = requests.put(url=url, headers=headers, params=params)
        if response.status_code != 201:
            exit(f'Ошибка YD {response.status_code}')

    def upload_photo(self, ydisk_file_path, url):
        """
        Загружает файл на яндекс диск по ссылке.
        :param ydisk_file_path: расположение и имя файла на яндекс диске
        :param url: ссылка на файл
        :return: в случае ошибки - код ошибки
        """
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {"path": ydisk_file_path, 'url': url}
        response = requests.post(url=upload_url, headers=headers, params=params)
        if response.status_code != 202:
            exit(f'Ошибка YD {response.status_code}')
        return response.status_code
