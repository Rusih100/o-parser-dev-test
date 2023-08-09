# rusih100-test-o-parser   
_REST API на Django Rest Framework с парсером маркетплейса._

## Описание   
Проект состоит из REST API на _Django Rest Framework_. Парсер реализован библиотекой _Selenium_ с помощью отложенных задач _Celery_. Уведомление о загруженных товарах и ошибках во время парсинга отправляются пользователю через telegram-бота. В проекте используются такие базы данных, как _MySQL_ и _Redis_. Документирование API осуществляется с помощью библиотеки _Django drf-yasg_. Панель администратора  кастомизирована с использованием AdminLTE. 

## Стек технологий
- Python
- Django Rest Framework
- MySQL
- Redis
- Selenium
- Celery
- Docker-compose
- git

## API endpoints
`POST api/v1/products/` - Запуск задачи на парсинг N товаров. Количество товаров должно принимается в теле запроса в параметре products_count, по умолчанию 10, максимум 50.   
   
`GET api/v1/products/` - Получение списка товаров.   
   
`GET api/v1/products/{product_id}/` - Получение товара по айди.

## Документация и панель администратора
`swagger/` - endpoint к докуметации swagger.  
`redoc/` - endpoint к докуметации redoc.   

`admin/` - endpoint к панели администратора. 

## Запуск проекта
Проект запускается с помощью Docker-compose  

1. Загрузите репозиторий и перейдите в него:   
```git clone https://github.com/Rusih100/rusih100-test-o-parser.git```

2. Соберите контейнеры:   
```docker-compose build```
   
3. Запуск контейнеров:     
```docker-compose up```    
   
Контейнеры также можно запустить в фоне:    
```docker-compose up -d```   

Примечание: Для работы уведомлений необходимо предварительно написать боту /start.  

## Скринкаст админки
![Скринкаст](https://raw.githubusercontent.com/Rusih100/rusih100-test-o-parser/master/screencast_1.png?token=GHSAT0AAAAAACAJAY3FECVUWZHOD36HONZ4ZGLVWJA)
![Скринкаст](https://raw.githubusercontent.com/Rusih100/rusih100-test-o-parser/master/screencast_2.png?token=GHSAT0AAAAAACAJAY3EW4NM35ANUCPU5TRIZGLVXFA)

## TO DO
- Написать тесты
- Написать документацию
