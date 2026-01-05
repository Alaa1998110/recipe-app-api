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
COPY ./scripts /scripts

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
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser -D django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# Set path
ENV PATH="/scripts:/py/bin:$PATH"


# Switch user
USER django-user


CMD ["run.sh"]