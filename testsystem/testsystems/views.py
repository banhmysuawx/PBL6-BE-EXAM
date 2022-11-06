import os

from .models import category, test, question, answer

from rest_framework import generics, permissions, views
from rest_framework.exceptions import *
from rest_framework.permissions import IsAuthenticated
from utils import email_helper


class CategoryList(generics.ListCreateAPIView):
    queryset = category.objects.all().order_by('name')
    serializer_class = categorySerializer
    
