FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

RUN mkdir -p /app

WORKDIR /app

COPY config /app/config
COPY lms /app/lms
COPY users /app/users
COPY *.py init.sh /app/
COPY pyproject.toml /app/

RUN chmod 755 /app/init.sh

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
