from django.db import models

from ..answers.models import Answer
from ..questions.models import Question


# Create your models here.
class QuestionComment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_comment_fk')
    user_id = models.IntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_comment_fk')
    user_id = models.IntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
