FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./app/ /app/

# Run Migrations
RUN python /app/manage.py makemigrations
RUN python /app/manage.py migrate
