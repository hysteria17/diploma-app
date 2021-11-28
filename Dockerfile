FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:80", "wsgi:app"]