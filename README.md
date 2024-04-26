# QuizWiz

## Fully responsive application for quiz generation. 

## Features
- Generate quiz manually or using LLM (**OpenAI API key required**)
- Take a quiz
- Store results and statistics
- Share the quiz
- Take quiz anonymously (with shared link)
- Copy **Prompt** and use it as an input in one of the free web versions of LLM ([ChatGPT](https://chat.openai.com/), [Gemini](https://gemini.google.com/)) to generate questions (copy the response into **JSON tab** of the new quiz)

## Deployment
In order to run application in [Docker](docker.com) execute in terminal:
```shell
git clone https://github.com/MikerT86/quiz-wiz-app.git
cd quiz-ai-app
docker-compose up -d
```

Run application locally (MacOS/Linux). Python version 3.12:
```shell
git clone https://github.com/MikerT86/quiz-wiz-app.git
cd quiz-wiz-app
python -m venv env
source env/bin/activate
pip install -r requirements.py
python manage.py collectstatic
python manage makemigrations
python manage migrate
gunicorn app.wsgi --bind 127.0.0.1:8000
```
