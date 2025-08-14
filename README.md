## Home Work Django-DRF + Docker
### DRF: HW-1, HW-2, HW-3, HW-4, HW-5, HW-6
### Docker: HW1 

---
# Запуск с помощью docker-compose
## Настройка окружения и запуск с помощью docker-compose
#### Установка компонентов
- Установите docker для вашего дистрибутива ОС
- Установите docker-compose

#### Настройте переменные окружения:
- Необходимо создайть файл .env на основе .env.sample и заполнить значения переменных

#### Запуск проекта:
```
 docker-compose up -d
```
При запуске произойдет инициализация WEB приложения и БД.

#### Проверка работоспособности сервисов:
- backend:
```
# Зайдите в браузере по URL и авторизируйтесь как пользователь admin:
http://localhost:8000/admin/

# Для отображения лога в консоли выполните команду:
docker-compose logs -f backend
```
- db
```
# Выполните команду подставив реальные значения:
docker-compose exec db pg_isready -d [POSTGRES_DB] -U [POSTGRES_USER]

# Для отображения лога в консоли выполните команду:
docker-compose logs -f db
```
- redis
```
# Выполните команду:
docker-compose exec redis redis-cli ping

# Для отображения лога в консоли выполните команду:
docker-compose logs -f redis
```
- celery, celery_beat
```
# Для отображения лога в консоли выполните команду:
docker-compose logs -f celery celery_beat
```

### Загрузка тестовых данных
```
# Загрузка моделей из фикстуры с тестовыми данными
# Соблюдайте последовательность загрузки!!!

# 1. Загрузка фикстур пользователей:
docker-compose exec backend python ./manage.py loaddata users_model_fixture

# 2. Загрузка фикстур Курсов/Уроков:
docker-compose exec backend python ./manage.py loaddata lms_model_fixture

# 3. Загрузка фикстур платежей Курсов/Уроков:
docker-compose exec backend python ./manage.py loaddata users_payments_fixture
```

---

## Настройка окружения для запуска на хосте (без docker)
#### Предварительные требования
- Python 3.11
- PostgreSQL >=14


- Выполнить команды:
```
# Подготовка окружения
pip install poetry
poetry install --no-root

# Настройка БД PostgreSQL:
# Создать пользователя для работы с БД
sudo -u postgres psql -c "
CREATE USER [имя_пользователя] WITH ENCRYPTED PASSWORD '[пароль]';
"

# Создать БД с имением magazine
sudo -u postgres psql -c "CREATE DATABASE mailer;"

# Настроить доступ к БД для пользователя
sudo -u postgres psql -c "
ALTER DATABASE mailer OWNER TO [имя_пользователя];
GRANT ALL PRIVILEGES ON DATABASE mailer TO [имя_пользователя];
"
```
- Создать файл .env на основе .env.sample и заполнить значения переменных
- Запустить миграции для подготовки проекта:
```
# Запуск миграций
poetry run ./manage.py migrate
```

- Создать пользователя для администрирования через WEB-UI:
```
# Создание администратора через кастомную команду
# логин и пароль задается в .env файле

poetry run ./manage.py csu


# Добавление группы 'Moderators' через кастомную команду

poetry run ./manage.py add_moderator_group

```

### Загрузка тестовых данных
```
# Загрузка моделей из фикстуры с тестовыми данными
# Соблюдайте последовательность загрузки!!!

# 1. Загрузка фикстур пользователей:
docker-compose exec backend python ./manage.py loaddata users_model_fixture

# 2. Загрузка фикстур Курсов/Уроков:
docker-compose exec backend python ./manage.py loaddata lms_model_fixture

# 3. Загрузка фикстур платежей Курсов/Уроков:
docker-compose exec backend python ./manage.py loaddata users_payments_fixture
```

### Запуск проекта
```
# Запуск сервера
poetry run ./manage.py runserver
```

### Запуск тестов
```
# Запуск тестов со сбором покрытия
poetry run coverage run --source='.' manage.py test

# Генерация отчета покрытия тестами
poetry run coverage report
```
