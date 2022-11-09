from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timezone

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class CustomModel(models.Model):

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def soft_delete(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()

    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_at = None
            self.save()

    class Meta:
        abstract = True

    objects = CustomManager()
    
class category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class test(CustomModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    time_limit = models.IntegerField()
    percent_to_pass = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    
    def __str__(self):
        return self.name
    


class question(CustomModel):
    test = models.ForeignKey(test, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    is_multiple_choice = models.BooleanField(default=True)
    
    def __str__(self):
        return self.content + " " + str(self.test.name)


class answer(CustomModel):
    question = models.ForeignKey(question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content + " " + str(self.question.id) + " " + str(self.is_correct)
    

class result(models.Model):
    test = models.ForeignKey(test, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time = models.IntegerField()
    result = models.IntegerField()
    
    def __str__(self):
        return str(self.test.name) + " " + str(self.time) + " " + str(self.result)