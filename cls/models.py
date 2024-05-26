# myapp/models.py

from django.db import models
from django.contrib.auth.models import User

class QuestionSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    text = models.CharField(max_length=200)
    label = models.CharField(max_length=50,null=True)
    confidence = models.FloatField(null=True)
    question_set = models.ForeignKey(QuestionSet, related_name='questions', on_delete=models.CASCADE)
