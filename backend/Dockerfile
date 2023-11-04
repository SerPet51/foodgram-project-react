FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]