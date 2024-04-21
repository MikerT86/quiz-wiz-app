import json

from django.db import models
from django.contrib.auth.models import User

class ExtendedUser(User):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    openai_key = models.CharField(max_length=255, blank=True)
    
    def statistics(self):
        
        results = Results.objects.filter(user=self)
        quiz_list = Quiz.objects.filter(author=self)
        
        statistics = {
            'total_quizzes': len(quiz_list),
            'total_results': len(results),
            'total_hard': len(quiz_list.filter(level="Hard")),
            'total_medium': len(quiz_list.filter(level="Medium")),
            'total_easy': len(quiz_list.filter(level="Easy")),
            'total_passed': len(results),
            'passed_hard': len(results.filter(quiz__level="Hard")),
            'passed_medium': len(results.filter(quiz__level="Medium")),
            'passed_easy': len(results.filter(quiz__level="Easy")),
            'average_score': (100 * results.aggregate(models.Sum('questions_answered'))['questions_answered__sum'] / results.aggregate(models.Sum('total_questions'))['total_questions__sum']).__round__(2) if len(results) > 0 else 0,          
        }
        
        return statistics
    
    
class Option(models.Model):

    text = models.TextField(max_length=500)

    def __str__(self):
        return self.text
        

class Question(models.Model):

    text = models.TextField(max_length=500, default="")
    answer = models.IntegerField(default=0)
    options = models.ManyToManyField(Option, blank=True)
    
    def __str__(self):
        return self.text
        
    def set_answer(self, answer):
        self.answer = answer

    def set_text(self, text):
        self.text = text
        
    def delete(self, using=None, keep_parents=False):
        for option in self.options.all():
            option.delete()
            
        self.options.clear()
        return super().delete(using, keep_parents)
    
    
class Quiz(models.Model):

    LEVEL_CHOICES = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]

    author = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, default=ExtendedUser)
    topic = models.CharField(max_length=100, default="")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="Easy")
    description = models.TextField(default="General knowledge", max_length=200)
    questions = models.ManyToManyField(Question, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    number_questions = models.IntegerField(default=0)

    def __str__(self):
        return self.pk + "\\" + self.topic + "\\" + str(self.author)
                 
    def save_questions(self, questions_json):
        
        for question_data in questions_json:
            question = Question.objects.create(text=question_data['text'], answer=question_data['answer'])
            for option_text in question_data['options']:
                option = Option.objects.create(text=option_text)
                question.options.add(option)  # Add options to the question
                self.questions.add(question)  # Add question to the quiz through the intermediate model

        self.number_questions = self.questions.count() 
        
    def get_number_questions(self):
        return self.questions.count()
    
    def questions_to_string(self) -> str:
        """
        This function takes a Quiz model instance and returns a JSON string
        """
        data = {"data": []}
        for question in self.questions.all():
            # Prepare question data
            question_data = {
                "text": question.text,
                "options": [],
                "answer": question.answer,
                }
            # Get answer options (text representation)
            for option in question.options.all():
                question_data["options"].append(option.text)
                # Append question data to the list
            data["data"].append(question_data)
                
        return json.dumps(data, indent=4)

    def delete(self, using=None, keep_parents=False):
        for question in self.questions.all():
            question.delete()
            
        self.questions.clear()
        return super().delete(using, keep_parents)  
    
    def time_to_complete(self):
        
        return self.get_number_questions() * 30
    
    def get_results(self, user):
        try:
            return Results.objects.get(user=user, quiz=self)
        except Results.DoesNotExist:
            return Results.objects.create(user=user, quiz=self, total_questions=self.get_number_questions())
    
class Results(models.Model):

    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, default=ExtendedUser)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=Quiz)
    total_questions = models.IntegerField(default=0)
    questions_answered = models.IntegerField(default=0)
    details = models.JSONField(blank=True, null=True, default=list)
    passed = models.BooleanField(default=False)    

    def update(self, results_json):
        """
        Update the quiz results based on the provided data.

        Parameters:
            results_json (dict): The JSON data containing the user's answers for each question.

        Returns:
            None
        """
        self.set_total_questions()
        self.questions_answered = 0
        self.details = []
        
        for question in self.quiz.questions.all():
            user_answer = {
                'text': question.text,
                'options': [option.text for option in question.options.all()],
                'answer': int(results_json.get(f"question_{question.id}", -1)),
                'correct_answer': question.answer
            }
            
            self.questions_answered += user_answer['answer'] == question.answer
            self.details.append(user_answer)  # Add user answer to the list of details
        
        self.passed = self.questions_answered >= 0.8 * self.total_questions
            
    def percent_correct(self):
        return int(self.questions_answered / self.total_questions * 100).__round__(2)
    
    def set_total_questions(self):
        self.total_questions = self.quiz.get_number_questions()
        
    def __str__(self):
        return self.quiz.topic + "\n" + str(self.user) + "\n" + str(self.passed)
    
    @staticmethod
    def get_results_anonymous(quiz, results_json):
        questions_answered = 0
        details = []
        total_questions = quiz.get_number_questions()
        
        for question in quiz.questions.all():
            user_answer = {
                'text': question.text,
                'options': [option.text for option in question.options.all()],
                'answer': int(results_json.get(f"question_{question.id}", -1)),
                'correct_answer': question.answer
            }
            
            questions_answered += user_answer['answer'] == question.answer
            details.append(user_answer)  # Add user answer to the list of details
        
        passed = questions_answered >= 0.8 * total_questions
        
        return {"details": details, 
                "passed": passed,
                'quiz': quiz,
                'total_questions': total_questions
                }, int(questions_answered / total_questions * 100).__round__(2)
        
    