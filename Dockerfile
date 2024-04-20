FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY ./api ./api
COPY ./app ./app
COPY manage.py .
COPY ./main ./main
COPY .env .

RUN python3 manage.py migrate
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]