FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==20.1.0

# Скопировать всё необходимое содержимое
# той директории локального компьютера, где сохранён Dockerfile,
# в текущую рабочую директорию образа – /app.
COPY . .

# Выполнить в текущей директории команду терминала
# для установки зависимостей.
RUN pip install -r requirements.txt --no-cache-dir

# При старте контейнера запустить сервер разработки.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]