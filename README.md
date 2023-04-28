# Курсовая работа «Резервное копирование»

Программа для резервного копирования фотографий (по умолчанию 5) с профиля пользователя vk в облачное хранилище Яндекс.Диск.  


## Описание:
Программа:
1. Получает фотографии с профиля.
2. Сохраняет фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
3. Для имени фотографий использует количество лайков или лайки+дата, если лайков одинаковое количество. 
4. Сохраняет информацию по фотографиям в файл photos.json с результатами. 

### Входные данные:
Пользователь вводит:
1. Токен яндекс диска;
2. id пользователя vk;
3. Альбом, откуда нужно копировать фото: profile или wall.

### Выходные данные:
1. Файл photos.json с информацией по файлу:
```javascript
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
```
2. Измененный Я.диск, куда добавились фотографии.
