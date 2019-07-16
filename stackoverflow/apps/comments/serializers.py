from rest_framework import serializers
from .models import QuestionComment
from datetime import datetime
from django.utils.timezone import get_current_timezone


class PostQuestionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionComment
        fields = ('question_id', 'user_id', 'comment')
        read_only_fields = ('question_id', 'user_id',)


class UpdateQuestionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionComment
        fields = ('question_id', 'user_id', 'comment')
        read_only_fields = ('question_id', 'user_id',)

    def update(self, instance, validated_data):
        instance.comment = validated_data['comment']
        instance.updated_at = datetime.now(tz=get_current_timezone()).isoformat()
        instance.save()
        return instance
