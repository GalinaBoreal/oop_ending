from yd import YD
from vk import VK


def main():
    ya_token = (input('Введите токен яндекс диска: '))
    album_id = (input('Для выбора альбома введите profile или wall: '))
    user_id = (input('Введите ID пользователя VK: '))

    yd = YD(token=ya_token)
    vk = VK(album_id, user_id)
    data = vk.get_photo_data()
    yd.upload_photo(data)


if __name__ == '__main__':
    main()
