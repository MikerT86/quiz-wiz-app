# QuizWiz

## Fully responsive application for quiz generation. 

## Functionality
1. You can generate quiz manually or using LLM (**OpenAI API key required**)
2. You can take quizzes.
3. You can see the results and statistics.
4. You can share the quiz.
5. You can take quiz anonymously (with shared link)
6. You can copy **Prompt** and use it as an input in one of the free web versions of LLM ([ChatGPT](https://chat.openai.com/), [Gemini](https://gemini.google.com/)) to generate questions (copy the response into **JSON tab** of the new quiz)

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
