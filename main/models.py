from django.db import models
from django.utils import timezone

# Create your models here.

#Сущность "Cell"

class Cell(models.Model):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'
    IN_PROGRESS = 'IN_PROGRESS'
    DISABLED = 'DISABLED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSE, 'Close'),
        (IN_PROGRESS, 'In Progress'),
        (DISABLED, 'Disabled'),
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
    answer = models.OneToOneField('Answer', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['field_number']

    def __str__(self):
        return f'Клетка:  {self.id} Поле: {self.field.key} Тип: {self.cell_type.name} ' \
               f'Статус: {self.get_status_display()}'


#Сущность "Question"

class Question(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='question_images/', null=True)
    penalty = models.IntegerField(help_text="Штрафное время в секундах")
    location = models.TextField(null=True, help_text="Гео локация точки")

    def __str__(self):
        return f'{self.name}'


#Сущность "CellType"

class CellType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


#Сущность "Answer"

class Answer(models.Model):
    text = models.TextField()
    attachment = models.FileField(upload_to='answer_attachments/', null=True)

    def __str__(self):
        return f'{self.text}'


#Сущность "Field"

class Field(models.Model):
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)
    closed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.key}'
