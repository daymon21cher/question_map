from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Field
from .serializers import FieldSerializer, FieldCustomActionSerializer
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

