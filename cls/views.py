from django.shortcuts import render
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from django.http import HttpResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import questionSerializer


# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def gen(request):
    serializer = questionSerializer(data=request.data)
    if serializer.is_valid():
        question=serializer.data['question_text']
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model_name="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
        model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        classifier=(pipeline("zero-shot-classification",model=model,tokenizer=tokenizer))
        res= classifier(question, ['Evaluation-synthesis','Remembering','Understanding','Application','Analysis','Creating-Synthesis'])
        label=res['labels'][0]
        confidence=res['scores'][0]
        return Response({'question': question,'label':label,'confidence':confidence})
