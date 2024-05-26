# myapp/serializers.py

from rest_framework import serializers
from .models import Question, QuestionSet
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'label', 'confidence']

class QuestionSetSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionSet
        fields = ['id', 'user', 'created_at', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        question_set = QuestionSet.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(question_set=question_set, **question_data)
        return question_set
