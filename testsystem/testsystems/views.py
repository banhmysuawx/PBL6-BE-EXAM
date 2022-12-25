import os

from .models import category, test, question, answer
import datetime
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from utils import email_helper
from rest_framework.response import Response
from .serializers import CategorySerializer, TestSerializer, QuestionSerializer, AnswerSerializer, CreateTestSerializer, DoingTestSerializer, ResultSerializer
from .models import category, test, question, answer, result

class TestView(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = test.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TestSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        serializer = TestSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        queryset.delete()
        return Response("Deleted")
    
    
    def create(self, request):
        serializer = CreateTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            id_test = serializer.data['id']
            instance = test.objects.get(id=id_test)
            serializer = TestSerializer(instance)
            return Response(serializer.data)
        return Response(serializer.errors)
    

class DoTestView(viewsets.ModelViewSet):
    serializer_class = DoingTestSerializer
    queryset = test.objects.all()
    
    def doing_test(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        serializer = TestSerializer(queryset, many=True)
        respond_questions = request.data['questions']
        mark = 0
        for respond_question in respond_questions:
            question_id = respond_question['id']
            correct_answers = list(question.objects.get(id=question_id).answers.filter(is_correct=True).values_list('id', flat=True))
            if respond_question.get('answers') is not None:
                respond_answers = respond_question['answers']
                # print(str(correct_answers) + ":" + str(respond_answers))
                # print(set(correct_answers) == set(respond_answers))
                if set(respond_answers).issubset(correct_answers) and len(correct_answers) == len(respond_answers):
                            mark += 1    
        start_time = datetime.datetime.strptime(request.data['time_start'], '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.datetime.strptime(request.data['time_done'], '%Y-%m-%dT%H:%M:%SZ')
        time = (end_time - start_time).seconds / 60
        percent = mark/len(question.objects.filter(test=pk))*100
        percent = round(percent, 2)
        test_id = pk
        user_id = request.data['user_id']
        job_id = request.data['job_id']
        if result.objects.filter(test_id=test_id, user_id=user_id, job_id=job_id).exists():
            data = result.objects.get(test_id=test_id, user_id=user_id, job_id=job_id)
            data_result = ResultSerializer(data)
            return Response(
                {
                    "meta": {"message": "You have already done this test"},
                    "data": data_result.data
                },
            )
        result_data = {
            "test": pk,
            "user_id": request.data['user_id'],
            "job_id": request.data['job_id'],
            "time_start": start_time,
            "time_end": end_time,
            "time": time,
            "result": percent
        }
        # print(result_data)
        serializer = ResultSerializer(data=result_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    

class CategoryView(generics.ListCreateAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer
    

class ResultView(viewsets.ModelViewSet):
    queryset = result.objects.all()
    serializer_class = ResultSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ResultSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, user_id, job_id):
        queryset = self.get_queryset().filter(user_id=user_id, job_id=job_id)
        serializer = ResultSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, user_id, job_id):
        queryset = self.get_queryset().filter(user_id=user_id, job_id=job_id)
        queryset.delete()
        return Response("Deleted")

class QuestionView(viewsets.ModelViewSet):
    queryset = question.objects.all()
    serializer_class = QuestionSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)
