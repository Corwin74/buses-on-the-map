# Автобусы на карте Москвы

Веб-приложение показывает передвижение автобусов на карте Москвы.

<img src="screenshots/buses.gif">

## Как установить

Для работы веб-приложения нужен Python версии не ниже 3.7. Скачайте к себе репозиторий и установите зависимости:

```bash
pip install -r requirements.txt
```

## Как запустить
- Откройте в браузере файл index.html
- Запустите сервер:
```bash
python server.py
```
- Запустите имитатор движения автобусов:
```bash
python fake_bus.py
```
## Настройки

Внизу справа на странице можно включить отладочный режим логгирования и указать нестандартный адрес веб-сокета.

<img src="screenshots/settings.png">

Настройки сохраняются в Local Storage браузера и не пропадают после обновления страницы. Чтобы сбросить настройки удалите ключи из Local Storage с помощью Chrome Dev Tools —> Вкладка Application —> Local Storage.

Если что-то работает не так, как ожидалось, то начните с включения отладочного режима логгирования.

Значения всех аргументов заданы по умолчанию. Можно переопределить значения либо в командной строке (имеют приоритет), либо в файле `.env`  
- Адрес, на котором запускается серверная часть приложения. По умолчанию 127.0.0.1   
`-host 127.0.0.1`  
`HOST=`  
- Порт, на котором сервер принимает соединения от браузеров, по умолчанию 8000:  
`-browser_port 8000`  
`BROWSERS_PORT=8000`  
- Порт, на котором сервер принимает соединения от автобусов, по умолчанию 8080:  
`-bus_port 8080`  
`BUSES_SERVER_PORT=8080`  
- Уровень логирования, по умолчанию минимальный вывод сообщений, изменяется только из командной строки:  
`-v, -vv, -vvv`  

Утилита `fake_bus` имеет дополнительные параметры:  
- Количество маршрутов, по котором запускаются автобусы. По умолчанию: все доступные маршруты из подкаталога `routes`  
`-r 200`  
`ROUTES_NUMBER=`  
Если задать большее количество маршрутов, чем имеется данных, то фактически загрузятся все доступные маршруты.  
- Количество автобусов на маршруте, по умолчанию 1:  
`-b 3`  
`BUSES_PER_ROUTE=35`  
- Количество паралельных каналов, по которым передаются данные на сервер. По умолчанию - 5  
`-w 5`  
`WEBSOCKETS_NUMBER=5`  
- Префикс для задания `id` экземпляра утилиты, при запуске нескольких экземпляров, по умолчанию - '1'  
`-id 1`  
`EMULATOR_ID=1`

## Формат данных

Фронтенд ожидает получить от сервера JSON сообщение со списком автобусов:

```js
{
  "msgType": "Buses",
  "buses": [
    {"busId": "c790сс", "lat": 55.7500, "lng": 37.600, "route": "120"},
    {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670к"},
  ]
}
```

Те автобусы, что не попали в список `buses` последнего сообщения от сервера будут удалены с карты.

Фронтенд отслеживает перемещение пользователя по карте и отправляет на сервер новые координаты окна:

```js
{
  "msgType": "newBounds",
  "data": {
    "east_lng": 37.65563964843751,
    "north_lat": 55.77367652953477,
    "south_lat": 55.72628839374007,
    "west_lng": 37.54440307617188,
  },
}
```



## Используемые библиотеки

- [Leaflet](https://leafletjs.com/) — отрисовка карты
- [loglevel](https://www.npmjs.com/package/loglevel) для логгирования


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
