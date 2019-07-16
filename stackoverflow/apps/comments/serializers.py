from rest_framework import serializers
from .models import QuestionComment, AnswerComment
from datetime import datetime
from django.utils.timezone import get_current_timezone


class PostQuestionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionComment
        fields = ('id', 'question_id', 'user_id', 'comment')
        read_only_fields = ('id', 'question_id', 'user_id',)


class UpdateQuestionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionComment
        fields = ('id', 'question_id', 'user_id', 'comment')
        read_only_fields = ('id', 'question_id', 'user_id',)

    def update(self, instance, validated_data):
        instance.comment = validated_data['comment']
        instance.updated_at = datetime.now(tz=get_current_timezone()).isoformat()
        instance.save()
        return instance


class PostAnswerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerComment
        fields = ('id', 'answer_id', 'user_id', 'comment')
        read_only_fields = ('id', 'answer_id', 'user_id',)


class UpdateAnswerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerComment
        fields = ('id', 'answer_id', 'user_id', 'comment')
        read_only_fields = ('id', 'answer_id', 'user_id',)

    def update(self, instance, validated_data):
        instance.comment = validated_data['comment']
        instance.updated_at = datetime.now(tz=get_current_timezone()).isoformat()
        instance.save()
        return instance
