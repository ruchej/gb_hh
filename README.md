# gb_hh
Учебный проект сайта для поиска работы


В файле .env переменные SECRET_KEY и ALLOWED_HOSTS указываются в виде списка
Файл .env располагать в директории файла settings.py

Для заполнения/очистки базы тестовыми данными можно использовать управляющую команду:
python manage.py update_db

## Запуск на сервере

1. Собираем images и запускаем контейнеры:
    `docker-compose up -d --build`
2. Создаем миграции в контейнере:
    `docker-compose exec backend python manage.py makemigrations`
3. Выполняем миграции в контейнере:
    `docker-compose exec backend python manage.py migrate`
4. Заполняем города в контейнере:
    `docker-compose exec backend python manage.py cities_light_fixtures load`
5. Заполняем базу из фикстур в контейнере:
    `docker-compose exec backend python manage.py update_db -j`
