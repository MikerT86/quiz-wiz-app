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
1. ```git clone https://github.com/MikerT86/quiz-wiz-app.git```
2. ```cd quiz-ai-app```
4. ```docker-compose up -d```

Run application locally (MacOS/Linux). Python version 3.12:
1. ```git clone https://github.com/MikerT86/quiz-wiz-app.git```
2. ```cd quiz-ai-app```
3. ```python -m venv env```
4. ```source env/bin/activate```
5. ```python manage.py collectstatic```
6. ```python manage makemigrations```
7. ```python manage migrate```
8. ```gunicorn app.wsgi --bind 127.0.0.1:8000```
