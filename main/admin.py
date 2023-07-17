from django.contrib import admin
from .models import Field
from .models import Cell
from .models import CellType
from .models import Answer
from .models import Question


class FieldAdmin(admin.ModelAdmin):
    fields = ['key', 'created_at', 'closed_at']
    readonly_fields = ['created_at', 'closed_at']


class CellAdmin(admin.ModelAdmin):
    fields = ['field_number', 'status', 'cell_type', 'field', 'question']
    list_display = ['__str__', 'field', 'status', 'id']


class CellTypeAdmin(admin.ModelAdmin):
    fields = ['name']


class AnswerAdmin(admin.ModelAdmin):
    fields = ['text', 'attachment']


class QuestionAdmin(admin.ModelAdmin):
    fields = ['name', 'text', 'image', 'penalty', 'answer']
    list_display = ['__str__', 'name', 'text', 'answer']


admin.site.register(Field, FieldAdmin)
admin.site.register(Cell, CellAdmin)
admin.site.register(CellType, CellTypeAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
