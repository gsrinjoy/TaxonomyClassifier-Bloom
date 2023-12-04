from rest_framework import serializers

class questionSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=200)
