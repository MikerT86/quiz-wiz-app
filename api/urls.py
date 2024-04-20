from django.urls import path, include
from . import views



urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('prompt/', views.get_prompt, name='get_prompt'),
    path('questions/', views.generate_questions, name='generate_questions'),
]
