FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./api ./api
COPY ./app ./app
COPY manage.py .
COPY ./main ./main
COPY .env .

RUN python manage.py migrate
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]