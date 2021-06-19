FROM python:3.9.5-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install elasticsearch google-api-python-client

CMD [ "python", "./search.py" ]