FROM python:3.9-alpine3.13

LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add --no-cache \
    python3-dev \
    build-base \
    libffi-dev \
    postgresql-dev \
    musl-dev

# Copy requirements
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy app
COPY ./app /app
WORKDIR /app

EXPOSE 8000

# Arguments
ARG DEV=false
ENV DEV=${DEV}

# Create virtualenv & install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser -D django-user

# Set path
ENV PATH="/py/bin:$PATH"

# Switch user
USER django-user
