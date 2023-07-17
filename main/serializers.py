from django.contrib.auth.models import User, Group
from rest_framework import serializers

from main.models import Question


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'name', 'text', 'answer', 'penalty')
