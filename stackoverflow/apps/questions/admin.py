from django.contrib import admin
from .models import Question, Rating, Votes, Tag

# Register your models here.
admin.site.register(Question)
admin.site.register(Rating)
admin.site.register(Votes)
admin.site.register(Tag)
