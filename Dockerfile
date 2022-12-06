FROM python:3.11.0-alpine

ENV PYTHONUNBUFFERED 1

RUN apk --no-cache update \
    && apk add bash \ 
                gcc \
                g++ \
                libc-dev \
                musl-dev \
                libffi-dev \
                git \
                npm \
                python3-dev

WORKDIR /softpage_note_api
COPY poetry.lock pyproject.toml .
RUN pip install --upgrade pip \
    && pip install "poetry==1.2.2" \
    && poetry config virtualenvs.create false \
    && poetry install --no-root
COPY . /softpage_note_api/

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

EXPOSE 8000
