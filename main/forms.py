from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Quiz, Results, ExtendedUser

QUESTIONS_TEMPLATE = '''{
    "data": [
        {
            "text": "Question text",
            "options": [
                "Option 1", 
                "Option 2", 
                ...
            ],
            "answer": 1
        },
        ...
    ]
}'''
    
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    openai_key = forms.CharField(max_length=100, required=False, label="OpenAI API key")
    
    class Meta:
        model = ExtendedUser
        fields = ("username", "email", "openai_key", "password1", "password2")


class QuizForm(forms.ModelForm):
    
    topic = forms.CharField(max_length=100, label="Topic", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter topic', 'id': 'topic', 'name': 'topic'}
    ))

    description = forms.CharField(max_length=500, required=True, label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter description', 'style': 'height: 60px; width: 100%;',
               'id': 'description', 'name': 'description'}
    ))

    questions_as_json = forms.CharField(required=True, label="Questions",
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': QUESTIONS_TEMPLATE,
                                    'style': 'height: 400px; width: 100%;',
                                    'id': 'questions',
                                    'name': 'questions',}))
    
    level = forms.ChoiceField(choices=Quiz.LEVEL_CHOICES, required=True, widget=forms.RadioSelect(), initial='Easy')

    class Meta:
        model = Quiz
        fields = ("topic", "description", "level", "questions_as_json")


class ResultsForm(forms.ModelForm):
    
    class Meta:
        model = Results
        fields = ("quiz", "user", "passed", "details")
        

class RunQuizForm(forms.Form):
    
    topic = forms.CharField(max_length=100, label="Topic", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter topic', 'id': 'topic', 'name': 'topic'}
    ))

    description = forms.CharField(max_length=500, required=False, label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter description', 'style': 'height: 50px; width: 100%;',
               'id': 'description', 'name': 'description'}
    ))
    
    class Meta:
        model = Quiz
        fields = ("topic", "description", "level", "questions", "number_questions")
