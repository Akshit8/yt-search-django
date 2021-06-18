FROM python:3.9.5-alpine

COPY . .

RUN pip install elasticsearch google-api-python-client

CMD [ "python", "./search.py" ]