from rest_framework import serializers
from .models import Answer, Votes
from datetime import datetime
from django.utils.timezone import get_current_timezone


class PostAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'user_id', 'body', 'created_at', 'updated_at')
        read_only_fields = ('id', 'question_id', 'user_id',)


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'user_id', 'body', 'created_at', 'updated_at')
        read_only_fields = ('id', 'question_id', 'user_id', 'created_at')

    def update(self, instance, validated_data):
        instance.body = validated_data['body']
        instance.updated_at = datetime.now(tz=get_current_timezone()).isoformat()
        instance.save()
        return instance


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ('id', 'user_id', 'up_vote', 'down_vote', 'answer_id')
        read_only_fields = ('id', 'user_id', 'answer_id')
