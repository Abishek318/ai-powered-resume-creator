FROM python:3.10-alpine AS builder
 
RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]