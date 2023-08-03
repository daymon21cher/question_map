from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Field, Cell, Answer
from .serializers import FieldSerializer, FieldCustomActionSerializer, CellSerializer, AnswerSimpleSerializer
from main.models import Question
from main.serializers import UserSerializer, QuestionSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []


class CellViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    permission_classes = []

    @action(detail=True, methods=['put'])
    def in_progress(self, request, pk):
        cell = self.get_object()
        cell.status = 'IN_PROGRESS'
        cell.save()
        Cell.objects.filter(
            field_id=cell.field_id, status=Cell.CLOSE
        ).exclude(id=cell.id).update(status=Cell.DISABLED)
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def take_answer(self, request, pk):
        serializer = AnswerSimpleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cell = self.get_object()
        print(serializer.data.get('text'))
        user_text = serializer.data.get('text')

        if cell.cell_type_id == 8 and user_text not in cell.question.variants:
            return Response(status=400, data={'reason': 'Bad Answer'})

        answer = Answer.objects.create(text=serializer.data.get('text'))
        cell.answer = answer
        cell.status = Cell.OPEN
        cell.save()
        Cell.objects.filter(
            field_id=cell.field_id, status=Cell.DISABLED
        ).exclude(id=cell.id).update(status=Cell.CLOSE)

        if self.check_field(cell.field_id):
            field = cell.field
            field.closed_at = timezone.now()
            field.save()
            return Response(status=201)
        return Response(status=200)

    @staticmethod
    def check_field(field_id):
        if Cell.objects.filter(field_id=field_id, status=Cell.OPEN, cell_type_id=8).count() == 9:
            return True
        if (
                Cell.objects.filter(field_id=field_id, status=Cell.OPEN, cell_type_id=8).count() == 8 and
                Cell.objects.filter(field_id=field_id, status=Cell.OPEN, cell_type_id=2).count() == 1
        ):
            return True
        return False


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = []

    @action(detail=False, methods=['get'], serializer_class=FieldCustomActionSerializer)
    def custom_action(self, request, pk=None):
        instance = self.get_queryset().filter(key=request.session.get('field_key', '')).first()
        if not instance:
            print(request.session.session_key)
            return Response(status=404)
        print(request.session.session_key)
        serializer = FieldCustomActionSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def login(self, request):
        print(request.session.session_key)
        session = request.session
        session['field_key'] = request.data['field_key']
        session.save()
        print(request.session.session_key)
        print(request.session['field_key'])
        field = Field.objects.filter(key=session['field_key']).first()
        if not field:
            return Response(status=404)
        if field.created_at is None:
            field.created_at = timezone.now()
            field.save(update_fields=['created_at'])
        return Response(status=200)
