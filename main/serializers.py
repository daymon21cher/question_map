from django.contrib.auth.models import User, Group
from rest_framework import serializers

from main.models import Question, Field, Cell, CellType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'name', 'text', 'penalty', 'location')

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('key', 'created_at', 'closed_at')


class CellTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellType
        fields = '__all__'


class CellSerializer(serializers.ModelSerializer):
    cell_type = CellTypeSerializer()
    question = serializers.SerializerMethodField()

    def get_question(self, instance):
        if instance.status == Cell.IN_PROGRESS and instance.question:
            return QuestionSerializer(instance.question).data
        else:
            return instance.question_id

    class Meta:
        model = Cell
        fields = ('id', 'field_number', 'status', 'field', 'question', 'cell_type')



class FieldCustomActionSerializer(serializers.ModelSerializer):
    cell_set = CellSerializer(many=True)

    class Meta:
        model = Field
        fields = ('key', 'created_at', 'closed_at', 'cell_set')


class AnswerSimpleSerializer(serializers.Serializer):
    text = serializers.CharField()