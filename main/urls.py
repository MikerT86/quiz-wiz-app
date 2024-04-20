from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('register', views.sing_up, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:pk>/', views.view_quiz, name='view_quiz'),
    path('quiz/update/<int:pk>', views.update_quiz, name='update_quiz'),
    # path('quiz/create_questions/', views.create_questions, name='create_questions'),
    path('quiz/delete/<int:pk>', views.delete_quiz, name='delete_quiz'),
    path('quiz/run/<int:pk>', views.run_quiz, name='run_quiz'),
    path('results/<int:pk>', views.results, name='results'),
    # path('quiz/run/<int:pk><str:username><str:email>', views.run_quiz, name='run_quiz'),
]
    