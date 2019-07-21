from django.db import models
from ..questions.models import Question


# Create your models here.
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_qn_fk')
    user_id = models.IntegerField(default=0)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    up_votes = models.IntegerField(default=0)


class Votes(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_rating_fk')
    user_id = models.IntegerField()
    up_vote = models.BooleanField(default=False)
    down_vote = models.BooleanField(default=False)
