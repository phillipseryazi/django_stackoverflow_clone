from django.template.defaultfilters import slugify
from rest_framework import serializers
from datetime import datetime
from django.utils.timezone import get_current_timezone

from .models import Question, Votes


class PostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'slug', 'body', 'is_open', 'is_resolved', 'is_closed', 'user_id')
        read_only_fields = ('slug', 'user_id')

    def get_slug(self, title):
        return slugify(f'{title}{datetime.now().isoformat()}')


class UpdateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'body')

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.body = validated_data['body']
        instance.updated_at = datetime.now(tz=get_current_timezone()).isoformat()
        instance.save()
        return instance


class CloseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('is_closed',)

    def update(self, instance, validated_data):
        instance.is_closed = validated_data['is_closed']
        instance.updated_at = datetime.now(tz=get_current_timezone()).isoformat()
        instance.save()
        return instance


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ('id', 'user_id', 'up_vote', 'down_vote', 'question_id')
        read_only_fields = ('id', 'user_id', 'question_id')
