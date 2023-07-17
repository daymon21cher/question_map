from django.db import models
from django.utils import timezone

# Create your models here.

#Сущность "Cell"

class Cell(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSE', 'Close'),
        ('IN_PROGRESS', 'In Progress'),
        ('DISABLED', 'Disabled'),
    ]

    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    field_number = models.IntegerField()
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='OPEN',
    )
    field = models.ForeignKey('Field', on_delete=models.CASCADE)
    cell_type = models.ForeignKey('CellType', on_delete=models.CASCADE)

    class Meta:
        ordering = ['field_number']


#Сущность "Question"

class Question(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='question_images/', null=True)
    penalty = models.IntegerField(help_text="Штрафное время в секундах")
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True)


#Сущность "CellType"

class CellType(models.Model):
    name = models.CharField(max_length=255)


#Сущность "Answer"

class Answer(models.Model):
    text = models.TextField()
    attachment = models.FileField(upload_to='answer_attachments/', null=True)

    def __str__(self):
        return f'answer {self.id}'


#Сущность "Field"

class Field(models.Model):
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(null=True)