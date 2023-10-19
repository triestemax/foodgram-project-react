## Проект Foodgram
Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc.
### Требуется установка Docker
Проект поставляется в четырех контейнерах Docker (db, frontend, backend, nginx).  
Для запуска необходимо установить Docker и Docker Compose. 
### База данных и переменные окружения
Проект использует базу данных PostgreSQL.  
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл ".env" с переменными окружения в папке "./infra/".

Шаблон для заполнения файла ".env":

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='Здесь указать секретный ключ django backend'
ALLOWED_HOSTS='Здесь указать имя или IP хоста' (Для локального запуска - localhost)

### Запускаем проект
Выполните команду docker-compose up -d --buld в папке "./infra/".
Выполните миграции docker-compose exec backend python manage.py migrate.
Создайте суперюзера docker-compose exec backend python manage.py createsuperuser.
Соберите статику docker-compose exec backend python manage.py collectstatic --no-input.
Заполните базу ингредиентами и нектороыми тегами docker-compose exec backend python manage.py command_csv.
###  Проект доступен
https://triestefoodgram.myddns.me/
вход в админку: maxim
пароль: 164532
### Автор
Максим Шабанов
[https://github.com/triestemax](https://github.com/triestemax)
