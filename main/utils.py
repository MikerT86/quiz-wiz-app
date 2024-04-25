from django.core.mail import send_mail
from django.db import models
from .models import Quiz, Results

def send_results_email(results, name, email, quiz):
    subject = f"Quiz Results: {quiz.topic}_{quiz.description}"
    message = f"Name: {name}\nEmail: {email}\nScore: {results['score']}% | Passed: {results['passed']}\n\n"
    
    details = ""
    for i, question in enumerate(results['details']):
        details += f"{i + 1}. Question: {question['text']} - {'Correct' if question['answer'] == question['correct_answer'] else 'Incorrect'}\n"
        details += "-"*50 + "\n"
        details += f"Options: \n{'\n'.join(question['options'])}\n"
        details += "-"*50 + "\n"
        details += f"Your Answer: {question['options'][question['answer'] - 1]}\n"
        details += f"Correct Answer: {question['options'][question['correct_answer'] - 1]}\n\n"
    
    message += details
    # Additional details in message (optional)
    send_mail(
        subject,
        message,
        'example@gmail.com',  # Replace with your email address
        [email],  # Recipient email
    )
    
def collect_statistics(results, quiz_list):
        
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