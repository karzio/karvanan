# Stage 1: Base with dependencies
ARG PYTHON_VERSION=3.12
ARG BASE_IMAGE=base

FROM python:${PYTHON_VERSION}

RUN apt update && \
    apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

ARG POETRY_VERSION=1.4.2

# Create a Python virtual environment for Poetry and install it
RUN python3 -m venv .venv && \
    pip install --upgrade pip && \
    pip install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install dependencies including Django
RUN poetry install --no-interaction --no-ansi

# Activate virtual environment and set PYTHONPATH
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH="$VIRTUAL_ENV/lib/python3.12/site-packages"

COPY . .

# Set permissions for entrypoint scripts
RUN chmod +x /app/docker/django/entrypoint.sh && \
    chmod +x /app/docker/tasks_app/entrypoint.sh

# Run Django application
CMD ["/bin/bash", "/app/docker/django/entrypoint.sh"]
