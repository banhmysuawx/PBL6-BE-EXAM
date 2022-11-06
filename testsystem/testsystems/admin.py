from django.contrib import admin
from .models import category, test, question, answer
# Register your models here.

admin.site.register(category)
admin.site.register(test)
admin.site.register(question)
admin.site.register(answer)