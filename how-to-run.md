- python 3.12 venv
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser --username=admin --email=admin@admin.com
  - Password: admin
  - Password (again): admin
  - Bypass password validation and create user anyway? [y/N]: y
- python manage.py runserver


Дальше надо зайти в админку по адресу /admin и залогиниться.
Теперь можно поиграться с добавлением и удалением ачивок, квестов, разных типов, проверить что с чем связано и все ли ок.
Еще я добавил коменты к моделям, чтобы было понятно что к чему.
Если все ок, думаю можно будет этот поц и развивать.
