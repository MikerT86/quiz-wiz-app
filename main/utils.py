from django.core.mail import send_mail

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