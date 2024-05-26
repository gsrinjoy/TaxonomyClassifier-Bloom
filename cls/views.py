# myapp/views.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from .serializers import UserSerializer, QuestionSetSerializer
from .models import QuestionSet,Question

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model_name = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gen(request):
    serializer = QuestionSetSerializer(data=request.data)
    if serializer.is_valid():
        questions_data = serializer.validated_data['questions']
        
        # Process questions and generate labels and confidences
        processed_questions = []
        for question_data in questions_data:
            question_text = question_data['text']
            res = classifier(question_text, ['Evaluation-synthesis', 'Remembering', 'Understanding', 'Application', 'Analysis', 'Creating-Synthesis'])
            label = res['labels'][0]
            print(res)
            confidence = res['scores'][0]
            processed_questions.append({'text': question_text, 'label': label, 'confidence': confidence})
        
        # Create QuestionSet and associated Questions
        question_set = QuestionSet.objects.create(user=request.user)
        for question in processed_questions:
            Question.objects.create(question_set=question_set, **question)
        
        return Response(QuestionSetSerializer(question_set).data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def results(request):
    user = request.user
    question_sets = QuestionSet.objects.filter(user=user).order_by('-created_at') # Adjust as needed
    serialized_data = QuestionSetSerializer(question_sets, many=True).data
    return Response(serialized_data)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"success": "Successfully logged out."}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
