# barter

## Описание

Проект **barter** создан для организации обмена вещами между пользователями. Пользователи могут размещать объявления о товарах для обмена, просматривать чужие объявления и отправлять предложения на обмен. Приложение имеет удобный веб-интерфейс, а также API для работы с объявлениями и обменными предложениями 

## Технологии

- Python 3.8+
- Django 4+
- Django REST Framework
- SQLite (по умолчанию)
- Boostrap5

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/WarfoIomey/barter.git
    ```
2. Перейдите в директорию проекта:
    ```bash
    cd barter
    ```
3. Установите виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```
4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
5. Выполните миграции:
    ```bash
    python manage.py migrate
    ```
6. (Опционально) Загрузите заготованные данные из файла db.json в базу данных:

    Учетная запись для входа
       - Логин: admin
       - Пароль: admin
    ```bash
    python manage.py loaddata db.json
    ```
7. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```