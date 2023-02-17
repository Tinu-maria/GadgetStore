FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
 
COPY . /app/

EXPOSE 8000

CMD ["python3","manage.py","runserver", "0.0.0.0:8000"]

# RUN command
# docker build -t app .
# docker run -p 8000:8000 app

