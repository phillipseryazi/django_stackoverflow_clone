from django.db import models
from ..users.models import User


# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_fk')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    is_open = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    up_votes = models.IntegerField(default=0)


class Rating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_rating_fk')
    likes = models.IntegerField()
    views = models.IntegerField()


class Votes(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_vote_fk')
    user_id = models.IntegerField()
    up_vote = models.BooleanField(default=False)
    down_vote = models.BooleanField(default=False)


class Tag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_tag_fk')
    tag = models.CharField(max_length=100)
