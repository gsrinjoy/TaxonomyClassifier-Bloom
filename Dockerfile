FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD gunicorn textxls.wsgi:application --bind 0.0.0.0:2000