FROM python:3.10-alpine as python

RUN apk update && apk add python3-dev libffi-dev musl-dev postgresql-dev gcc git openssl


COPY ./requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install --upgrade pip && pip install -r ./requirements.txt

WORKDIR /app
COPY . /app/


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
                 