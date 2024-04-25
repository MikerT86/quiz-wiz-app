from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import QGenerator
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_prompt(request):
    if 'numQuestions' not in request.data or 'topic' not in request.data or 'level' not in request.data:
        return Response(status=400, data={'message': 'Missing required fields (topic, level, numQuestions)'})
    
    return Response(QGenerator.prompt(request.data), status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_questions(request):
    if 'numQuestions' not in request.data or 'topic' not in request.data or 'level' not in request.data:
        return Response(status=400, data={'message': 'Missing required fields (topic, level, numQuestions)'})
    
    openAIKey = request.user.extendeduser.openai_key if not request.user.extendeduser.openai_key else request.data.get('openAIKey', '').strip()
    agent = QGenerator(user_key=openAIKey)
    
    return Response(agent.generate_questions(request.data), status=200)
    