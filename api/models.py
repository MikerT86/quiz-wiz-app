import os
import json
import time

from openai import OpenAI

PROMPT_TEMPLATE = '''
I want you to generate quiz questions on topic '{1}: {3}'. 
Please follow instructions:
1) Number of questions should be {0}
2) Difficulty level should be {2}
- If difficulty level is 'Easy', you should generate very common, well known and obvious questions.
- If difficulty level is 'Medium', the questions should cover general knowledge of the topic with some special cases.
- If difficulty level is 'Hard', you should ask advanced, tricky and rare questions on the topic.
3) Do not repeat options. 
4) All options should be close to the correct answer, but the only one of them should be correct.
5) Do not repeat questions
6) Do not make up questions or answers.
7) Number of possible answer options should be at least 2 but no more than 4.
8) Provide the questions in JSON format with the following key: 
    - The 'data' key should be present in the JSON. The value of 'data' key should be an array of questions.
    Each question should be an object with the following keys:
    - The 'text' key should have a value that represents the question. 
    - The 'options' key should have an array of options. 
    - The 'answer' key should be the correct option number starting from 1.
9) Do not include any other keys or text in the response.
10) If you not familiar with topic or it doesn't represent an object or process, respond with {{"message": "Unknown Topic"}}. Do not provide any explanation.
Use this template for your answer:
{{ 
    "data": [{{
        "text": "insert question text here", 
        "options": [insert answer options here in double quotes separated by comma],
        "answer": insert the number of correct option in the 'options' array
        }},
        ]
}}

Example of the generated JSON:
{{
  "data": [
        {{
        "text": "When using Promises in JavaScript, what happens if you throw an error inside a `.then()` callback?",
        "options": [
            "The error is silently ignored",
            "The Promise remains in a pending state",
            "The error is propagated to the next `.then()` or `.catch()`",
            "Only errors from the executor function are considered"
        ],
        "answer": 2
        }}
    ]
}}
'''


class QGenerator:
    
    _BASE_PROMT = PROMPT_TEMPLATE
    
    def __init__(self, model = 'gpt', user_key=None) -> None:
        self.model = model
        self.open_ai_key = os.environ.get('OPENAI_API_KEY', '') if user_key is None else user_key
        
    def generate_questions(self, data):

        if not self.open_ai_key:
            answer = self.template(data)
        else:
            prompt = self.prompt(data)
            answer = json.loads(self.run_api(prompt))
            
        return answer

    def get_base_prompt(self):
        return self._BASE_PROMT
    
    def template(self, data):
        
        questions = {'data': []}
            
        for i in range(int(data['numQuestions'])):
            question = {
                'text': 'Question ' + str(i + 1),
                'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
                'answer': 1
            }
            
            questions['data'].append(question)
        
        return questions
        
    def run_api(self, prompt):
        
        if self.model == 'gpt':
            client = OpenAI(api_key=self.open_ai_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                ).choices[0].message.content

        else:
            raise Exception('Model not found')
        
        return response
    
    @classmethod
    def prompt(cls, data):
        
        return cls._BASE_PROMT.format(data['numQuestions'], data['topic'], data['level'], data['description'])
