# Stage 1: Builder
FROM python:3-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache build-base

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runner
FROM python:3-alpine AS runner

WORKDIR /app

# Copy virtual environment and application code from builder stage
COPY --from=builder /app/venv venv
COPY . .

# Collect static files
RUN . venv/bin/activate && python manage.py collectstatic --noinput

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PORT=8000

# EXPOSE ${PORT}
# COPY ./entrypoint.sh /
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

CMD gunicorn --bind :${PORT} --workers 2 resumebot.wsgi:application

# docker build -t bot .  
# docker run -p 8000:8000 bot 