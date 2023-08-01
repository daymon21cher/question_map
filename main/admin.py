from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Field
from .models import Cell
from .models import CellType
from .models import Answer
from .models import Question


class CellAdminInline(TabularInline):
    extra = 1
    model = Cell
    readonly_fields = ('answer_text', 'question_variants', 'question_penalty')
    fields = (
        'id',
        'cell_type',
        'question',
        'field_number',
        'status',
        'answer_text',
        'question_variants',
        'question_penalty'
    )

    def answer_text(self, obj):
        if obj.answer:
            return obj.answer.text
        else:
            return ""

    def question_variants(self, obj):
        if obj.question:
            return obj.question.variants
        else:
            return []

    def question_penalty(self, obj):
        if obj.question:
            return obj.question.penalty
        else:
            return []

class FieldAdmin(admin.ModelAdmin):
    fields = ['key', 'created_at', 'closed_at', 'diff']
    readonly_fields = ['created_at', 'closed_at', 'diff']
    inlines = (CellAdminInline,)

    def diff(self, obj):
        if obj.created_at and obj.closed_at:
            delta = obj.closed_at - obj.created_at
            delta_arr = str(delta).split('.')
            return f'{delta_arr[0]}'
        else:
            return None


class CellAdmin(admin.ModelAdmin):
    fields = ['field_number', 'status', 'cell_type', 'field', 'question', 'answer']
    list_display = ['__str__', 'field', 'status', 'id', 'answer']


class CellTypeAdmin(admin.ModelAdmin):
    fields = ['name']


class AnswerAdmin(admin.ModelAdmin):
    fields = ['text', 'attachment']


class QuestionAdmin(admin.ModelAdmin):
    fields = ['name', 'text', 'image', 'penalty', 'variants']
    list_display = ['__str__', 'name', 'text']


admin.site.register(Field, FieldAdmin)
admin.site.register(Cell, CellAdmin)
admin.site.register(CellType, CellTypeAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
