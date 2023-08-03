# rusih100-test-o-parser   
_REST API на Django Rest Framework с парсером маркетплейса._

## Описание   
Проект состоит из REST API на _Django Rest Framework_. Парсер реализован библиотекой _Selenium_ с помощью отложенных задач _Celery_. Задачи _Celery_ отслеживаются с помощью _Flower_.  Уведомление о загруженных товарах и ошибках во время парсинга отправляются пользователю через telegram-бота. В проекте используются такие базы данных, как _MySQL_ и _Redis_. Документирование API осуществляется с помощью библиотеки _Django drf-yasg_. Панель администратора  кастомизирована с использованием AdminLTE. 

## Стек технологий
- Python
- Django Rest Framework
- MySQL
- Redis
- Selenium
- Celery
- Flower
- Docker-compose
- git

## API endpoints
`POST api/v1/products/` - Запуск задачи на парсинг N товаров. Количество товаров должно принимается в теле запроса в параметре products_count, по умолчанию 10, максимум 50.   
   
`GET api/v1/products/` - Получение списка товаров.   
   
`GET api/v1/products/{product_id}/` - Получение товара по айди.

## Запуск проекта

### 1. Загрузка репозитория
```git clone https://github.com/Rusih100/rusih100-test-o-parser.git```

### 2. Установка зависимостей
В проекте используется менеджер пакетов [Poetry](https://python-poetry.org/docs/).   

Команда _install_ считывает файл _pyproject.toml_ из текущего проекта, находит зависимости и устанавливает их.    
```poetry install```

### 3. Переменные окружения
Создайте и заполните файл _.env_ по примеру _example.env_

### 4. Запуск MySQL и Redis
Базы данных собираются мз файла docker-compose.yaml следующими двумя командами.   
Сборка образов:  
```docker-compose build```  
    
Запуск контейнеров:   
```docker-compose up```    
   
P.S. Контейнеры можно запустить в фоне:
```docker-compose up -d```   

### 5. Запуск Django  
Примените миграции:  
```python manage.py migrate```  
   
Соберите статические файлы:   
```python manage.py collectstatic```  
    
Создайте суперпользователя:   
```python manage.py createsuperuser```  
   
Запустите сервер Django:    
```python manage.py runserver```  
   
Запустите Flower (Опционально):    
```celery -A django_ozon_parser flower```   

Запустите Celery:  
```celery -A django_ozon_parser worker --loglevel=info --pool=solo```   

## Скринкаст админки
![Скринкаст](https://raw.githubusercontent.com/Rusih100/rusih100-test-o-parser/master/screencast_1.png?token=GHSAT0AAAAAACAJAY3FECVUWZHOD36HONZ4ZGLVWJA)
![Скринкаст](https://raw.githubusercontent.com/Rusih100/rusih100-test-o-parser/master/screencast_2.png?token=GHSAT0AAAAAACAJAY3EW4NM35ANUCPU5TRIZGLVXFA)

## TO DO
- Написать тесты
- Собрать Docker-контейнер для приложения Django
