# Курсовая работа "Онлайн-магазин по продаже автомобилей"

## Описание проекта

### Основные возможности

- Регистрация и аутентификация пользователей
- Просмотр каталога автомобилей
- Добавление и удаление товаров из корзины
- Оформление заказа
- Административная панель для управления товарами и заказами

### Технологии

- **Django:** Используется как основной веб-фреймворк для создания приложения.
- **Bootstrap:** Используется для создания стильного и отзывчивого интерфейса.
- **Миграции Django:** Для управления базой данных.
- **Тесты Django:** Используются TestCase для проверки функциональности.
- **GitHub Actions и GitLab CI:** Настроены для автоматической сборки и тестирования проекта.
- **pip-compile:** Для управления зависимостями Python.

## Установка

1. Клонирование репозитория:

```bash
git clone https://github.com/MikeMoore1337/django_carshop.git
cd django_carshop
```

2. Установка зависимостей:

```pip install -r requirements.txt```

3. Применение миграций:

```python manage.py migrate```

## Запуск

```python manage.py runserver```

После этого приложение будет доступно по адресу http://127.0.0.1:8000/.

## Тестирование

```python manage.py test```