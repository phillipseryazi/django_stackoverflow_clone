from django.contrib import admin
from .models import QuestionComment, AnswerComment

# Register your models here.
admin.site.register(QuestionComment)
admin.site.register(AnswerComment)
