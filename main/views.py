import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import transaction

from .forms import RegistrationForm, QuizForm
from .models import Quiz, Results

@login_required(login_url="/login")
def home(request):
    quiz_list = Quiz.objects.all().order_by('-created_at')
    results = Results.objects.filter(user=request.user)
    
    for quiz in quiz_list:
        if results.filter(quiz=quiz).exists():
            quiz.passed = results.get(quiz=quiz).passed
        else:
            quiz.passed = -1
    
    return render(request, 'home.html', {"quiz_list": quiz_list, "statistics": request.user.extendeduser.statistics()})


def sing_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required(login_url="/login")
def create_quiz(request):

    if request.method == "POST":
        form = QuizForm(request.POST)
       
        if form.is_valid():
            questions = json.loads(form.cleaned_data['questions_as_json'])['data']
            with transaction.atomic():
                quiz = Quiz.objects.create(
                        author=request.user.extendeduser,
                        topic=form.cleaned_data['topic'],
                        level=form.cleaned_data['level'],
                        description=form.cleaned_data['description'],
                    )
                quiz.save_questions(questions)
                quiz.save()
            transaction.commit()
            return redirect(f'/quiz/update/{quiz.id}')
        else:
            print(form.errors)
    else:
        form = QuizForm()

    return render(request, 'create_quiz.html', {'form': form, 'quiz': None})


def run_quiz(request, pk):
    
    quiz = Quiz.objects.get(pk=pk)
    if request.method == "GET" and request.user.is_anonymous:
        if request.GET.get('username', '') == '' or request.GET.get('email', '') == '':
            return redirect(f'/quiz/{pk}')
    
    if request.method == "POST":
        if request.user.is_anonymous:
            results, score = Results.get_results_anonymous(quiz, request.POST)
            return render(request, 'results.html', {'results': results, 'percent_correct': score})
        else:
            results = quiz.get_results(request.user.extendeduser)
            results.update(request.POST)
            results.save()
            return redirect(f'/results/{quiz.id}')
        
    return render(request, 'run_quiz.html', {'quiz': quiz, 'time_limit': quiz.time_to_complete()})



@login_required(login_url="/login")
def results(request, pk):
    
    try:
        results = Results.objects.get(user=request.user.extendeduser, quiz=Quiz.objects.get(pk=pk))
        return render(request, 'results.html', {'results': results, 'percent_correct': results.percent_correct()})
    except Results.DoesNotExist:
        messages.info(request, f"Results of the quiz: {request.GET['quiz_id']} for User {request.user.extendeduser} not found")
        return redirect('/')
    
@login_required(login_url="/login")
def delete_quiz(request, pk):
    
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'GET':
        quiz.delete()
        return redirect('/')

@login_required(login_url="/login")
def update_quiz(request, pk):
    
    quiz = Quiz.objects.get(pk=pk)

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            
            with transaction.atomic():
                quiz.author = request.user.extendeduser
                if quiz.questions_to_string() != form.cleaned_data['questions_as_json']:
                    for question in quiz.questions.all(): 
                        question.delete()
                    quiz.questions.clear()
                    quiz.save_questions(json.loads(form.cleaned_data['questions_as_json'])['data'])
                quiz.save()
            transaction.commit()
            redirect(f'/quiz/update/{quiz.id}')
        else:
            print(form.errors)
    else:
        form = QuizForm(instance=quiz, initial={'questions_as_json': quiz.questions_to_string()})

    return render(request, 'create_quiz.html', {'form': form, 'quiz': quiz})

def view_quiz(request, pk):
    
    quiz = Quiz.objects.get(pk=pk)
    time_to_complete = quiz.time_to_complete()
    
    minutes = time_to_complete // 60
    seconds = time_to_complete % 60
    time_repr = f"{seconds} sec" if minutes == 0 else f"{minutes} min and {seconds} sec"
    
    template = 'view_quiz_anonym.html' if request.user.is_anonymous else 'view_quiz.html'
    return render(request, template, {'quiz': Quiz.objects.get(pk=pk), 'time_limit': time_repr})
