FROM node:19-alpine as node-builder
COPY client /client
WORKDIR /client
RUN npm install && npm run generate

FROM python:3.10-alpine as python

RUN apk update && apk add python3-dev libffi-dev musl-dev postgresql-dev gcc git openssl


COPY ./requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install --upgrade pip && pip install -r ./requirements.txt

WORKDIR /app
COPY . /app/
COPY --from=node-builder /client/dist /app/client/dist


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
                 