# Foodgram
# Проект «Продуктовый помощник» - Foodgram
Foodgram - Продуктовый помощник. Сервис позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


# Порядок запуска
## На локальном компьютере:
Клонируйте репозиторий и перейдите каталок с файлом docker-compose.yaml:
```
git clone git@github.com:SerPet51/foodgram-project-react.git
cd infra
```
Создайте и активируйте виртуальное окружение, обновите pip и установите зависимости:
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
python3 -r requirements.txt
```
Создайте файл .env внутри папки infra:   
Внесите туда переменные окружения:   
```
SECRET_KEY
ALLOWED_HOSTS
DB_ENGINE=django.db.backends.postgresql
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
```
Запустите сборку контейнера с проектом командой:
```
docker-compose up -d --build
```
Соберите статические файлы (статику):
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Примените миграции:
```
docker-compose exec backend python manage.py makemigrations
```
```
docker-compose exec backend python manage.py migrate --noinput
```
Создайте суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
При необходимости заполните базу ингредиентов из recipes/data/:
```
docker-compose exec backend python manage.py load_data
```
##На удалённом сервере:
1. Клонируйте репозиторий на локальную машину командой:
 ```
 git clone git@github.com:SerPet51/foodgram-project-react.git
 ```
2. В вашем репозитории на гитхаб в  ```Settings - Secrets - Actions``` добавьте ключи
> DOCKER_USERNAME - имя пользователя docker;  
> DOCKER_PASSWORD - пароль docker;  
> HOST - ip-адрес сервера;  
> USER - имя пользователя для сервера;  
> SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу ``` cat ~/.ssh/id_rsa ```;  
> PASSPHRASE - пароль для сервера;  
> DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql;  
> DB_NAME=postgres - имя базы данных;  
> POSTGRES_USER - логин для подключения к базе данных;  
> POSTGRES_PASSWORD - пароль для подключения к БД;  
> DB_HOST=db - название сервиса (контейнера);  
> DB_PORT=5432 - порт для подключения к БД;  
> TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start);  
> TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота);
3. Измените имя пользователя DockerHub в docker-compose.yaml на ваше

### Подготовка сервера
- Запустите сервер и зайдите на него ``` ssh username@ip_address ```;
- Установите обновления apt:
``` sudo apt update ```;
``` sudo apt upgrade -y ```;  
- Установите nginx ``` sudo apt install nginx -y ```;
- Остановите службу nginx ``` sudo systemctl stop nginx ```;
- Установите docker ``` sudo apt install docker.io ```;
- Установите docker-compose: 
Выполните команду, чтобы загрузить текущую стабильную версию Docker Compose:  
``` sudo curl -SL https://github.com/docker/compose/releases/download/v2.6.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose ```;  
Примените к файлу права доступа:  
``` sudo chmod +x /usr/local/bin/docker-compose	```;  
Проверьте установку (должна вернуться версия docker-compose):  
``` docker-compose --version ```;  
- Создайте на сервере два файла и скопируйте в них код из проекта на GitHub:  
> docker-compose.yaml в home/<username>/docker-compose.yaml  
``` sudo nano docker-compose.yaml ```  
> nginx/default.conf в home/<username>/nginx/default.conf  
``` mkdir nginx ```  
``` sudo nano nginx/default.conf ```

#### Развертывание приложения на боевом сервере
При первоначальном развертывании будут автоматически применены миграции
и загружена первоначальная база данных, если не хотите этого, закомментируйте 
команды ```sudo docker-compose exec web ...``` внутри файла yamdb_workflow.yml  
Для запуска автоматического развертывания на сервере с помощью Actions workflow 
закоммитьте изменения в docker-compose.yaml и запуште их.  
За статусом работы можно проследить на вкладке Actions на GitHub.

Для создания суперользователя введите команду:  
```
sudo docker-compose exec web python createsuperuser
```


## Пользовательские роли в проекте
1. Анонимный пользователь
2. Аутентифицированный пользователь
3. Администратор

### Анонимные пользователи могут:
1. Просматривать список рецептов;
2. Просматривать отдельные рецепты;
3. Фильтровать рецепты по тегам;
4. Создавать аккаунт.

### Аутентифицированные пользователи могут:
1. Получать данные о своей учетной записи;
2. Изменять свой пароль;
3. Просматривать, публиковать, удалять и редактировать свои рецепты;
4. Добавлять понравившиеся рецепты в избранное и удалять из избранного;
5. Добавлять рецепты в список покупок и удалять из списка;
6. Подписываться и отписываться на авторов;
7. Скачать список покупок

### Набор доступных эндпоинтов:
- ```api/docs/redoc``` - Подробная документация по работе API.
- ```api/tags/``` - Получение, списка тегов (GET).
- ```api/ingredients/``` - Получение, списка ингредиентов (GET).
- ```api/ingredients/``` - Получение ингредиента с соответствующим id (GET).
- ```api/tags/{id}``` - Получение, тега с соответствующим id (GET).
- ```api/recipes/``` - Получение списка с рецептами и публикация рецептов (GET, POST).
- ```api/recipes/{id}``` - Получение, изменение, удаление рецепта с соответствующим id (GET, PUT, PATCH, DELETE).
- ```api/recipes/{id}/shopping_cart/``` - Добавление рецепта с соответствующим id в список покупок и удаление из списка (GET, DELETE).
- ```api/recipes/download_shopping_cart/``` - Скачать файл со списком покупок TXT (в дальнейшем появиться поддержка PDF) (GET).
- ```api/recipes/{id}/favorite/``` - Добавление рецепта с соответствующим id в список избранного и его удаление (GET, DELETE).

#### Операции с пользователями:
- ```api/users/``` - получение информации о пользователе и регистрация новых пользователей. (GET, POST).
- ```api/users/{id}/``` - Получение информации о пользователе. (GET).
- ```api/users/me/``` - получение и изменение данных своей учётной записи. Доступна любым авторизованными пользователям (GET).
- ```api/users/set_password/``` - изменение собственного пароля (PATCH).
- ```api/users/{id}/subscribe/``` - Подписаться на пользователя с соответствующим id или отписаться от него. (GET, DELETE).
- ```api/users/subscribe/subscriptions/``` - Просмотр пользователей на которых подписан текущий пользователь. (GET).

#### Аутентификация и создание новых пользователей 👇:
- ```api/auth/token/login/``` - Получение токена (POST).
- ```api/auth/token/logout/``` - Удаление токена (POST).

#### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос для регистрации нового пользователя с параметрами
***email username first_name last_name password***
на эндпойнт ```/api/users/```
2. Пользователь отправляет POST-запрос со своими регистрационными данными ***email password*** на эндпоинт ```/api/token/login/``` , в ответе на запрос ему приходит auth-token. Примечание: При взаимодействии с фронтэндом приложения операция два происходит под капотом при переходе по эндпоинту ```/api/token/login/```.

Подробнее о методах API можно узнать после сборки контейнера по ссылке:
```
http://localhost/api/docs/redoc.html
```

### Посетить сайт можно по ссылке
```
https://62.84.120.183/recipes
https://foodgramyap.ddns.net/recipes
```

Автор:   
Петров Сергей - https://github.com/SerPet51