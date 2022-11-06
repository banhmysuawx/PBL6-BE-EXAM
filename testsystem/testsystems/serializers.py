from rest_framework import serializers
from .models import category, test, question, answer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at', 'description']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = ['id', 'name', 'category', 'time_limit', 'percent_to_pass', 'description', 'created_at', 'updated_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = ['id', 'test', 'content', 'is_multiple_choice', 'description', 'created_at', 'updated_at']
    

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer
        fields = ['id', 'question', 'content', 'is_correct', 'description', 'created_at', 'updated_at']
        

class QuestionForTestSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = question
        fields = ['id', 'test', 'content', 'is_multiple_choice', 'answers', 'description', 'created_at', 'updated_at']



class CreateTestSerializer(serializers.ModelSerializer):
    questions = QuestionForTestSerializer(many=True)
    class Meta:
        model = test
        fields = ['id', 'name', 'category', 'time_limit', 'percent_to_pass', 'questions', 'description', 'created_at', 'updated_at']
        read_only_fields = ('update_at', 'is_active')

    def create(self, validated_data):
        return test.objects.create(**validated_data)