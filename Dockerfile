FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY backend/requirements.txt /code/
RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY backend/wait-for-db.sh /code/
RUN chmod +x /code/wait-for-db.sh

COPY backend/ /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/code/wait-for-db.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"] 