from rest_framework import serializers
from .models import category, test, question, answer, result


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at', 'description']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer
        fields = ['id', 'content', 'is_correct', 'question']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = question
        fields = ['id','content', 'answers', 'is_multiple_choice', 'test']


class TestSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True, read_only=True)
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = test
        fields = ['id', 'name', 'category', 'time_limit', 'questions', 'percent_to_pass', 'description', 'created_at', 'updated_at']

class AnswerForQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer
        fields = ['content', 'is_correct']



class QuestionForTestSerializer(serializers.ModelSerializer):
    answers = AnswerForQuestionSerializer(many=True)
    is_multiple_choice = serializers.BooleanField(default=True)
    class Meta:
        model = question
        fields = ['content', 'is_multiple_choice', 'answers']



class CreateTestSerializer(serializers.ModelSerializer):
    questions = QuestionForTestSerializer(many=True)
    class Meta:
        model = test
        fields = ['id', 'name', 'category', 'time_limit', 'percent_to_pass', 'questions', 'description', 'created_at', 'updated_at']
        read_only_fields = ('update_at', 'is_active','id')

    def create(self, validated_data):
        validated_data_temp = validated_data.copy()
        questions = validated_data_temp.pop('questions')
        test_data ={
            "name": validated_data_temp['name'],
            "category": validated_data_temp['category'].id,
            "time_limit": validated_data_temp['time_limit'],
            "percent_to_pass": validated_data_temp['percent_to_pass'],
            "description": validated_data_temp['description'],
        }
        serializer_test = TestSerializer(data=test_data)
        serializer_test.is_valid(raise_exception=True)
        test = serializer_test.save()
        validated_data["id"] = test.id
        try:
            for question in questions:
                question_data = {
                    "content": question['content'],
                    "is_multiple_choice": question['is_multiple_choice'],
                    "test": test.id
                }
                serializer_question = QuestionSerializer(data=question_data)
                serializer_question.is_valid(raise_exception=True)
                id_question = serializer_question.save().id
                for answer in question['answers']:
                    answer_data = {
                        "content": answer['content'],
                        "is_correct": answer['is_correct'],
                        "question": id_question
                    }
                    serializer_answer = AnswerSerializer(data=answer_data)
                    serializer_answer.is_valid(raise_exception=True)
                    serializer_answer.save()
        except Exception as e:
            test.delete()
            raise serializers.ValidationError(e)
        
        return validated_data


class QuestionForDoingTestSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(child=serializers.IntegerField(required=True))
    id = serializers.IntegerField(required=True)
    class Meta:
        model = question
        fields = ['id', 'answers']

class DoingTestSerializer(serializers.ModelSerializer):
    questions=QuestionForDoingTestSerializer(many=True, read_only=True)
    id = serializers.IntegerField(source='pk', read_only=True)
    time_done = serializers.DateTimeField(required=True)
    time_start = serializers.DateTimeField(required=True)
    class Meta:
        model = test
        fields = ['id','questions', 'time_done', 'time_start']
        
    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
    
    
class ResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = result
        fields = '__all__'