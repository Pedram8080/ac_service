FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY backend/requirements.txt /code/
RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY backend/ /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 