# Stage 1: Builder
FROM python:3-alpine AS builder

WORKDIR /app

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: Runner
FROM python:3-alpine AS runner

WORKDIR /app

COPY --from=builder /app/venv /app/venv
COPY resumebot /app/resumebot

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PORT=8000

EXPOSE ${PORT}

CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "--workers", "2", "resumebot.wsgi:application"]
