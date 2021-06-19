# alpine based python image
FROM python:3.9.5-alpine

# setting up workdir, better for multistage builds
WORKDIR /app

# setting environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# setting stage variables for django
ENV DEBUG_MODE=false

COPY . .

# installing application dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# exposing port
EXPOSE 8000

# migration and starting application
CMD ./manage.py migrate && \
        ./manage.py runserver