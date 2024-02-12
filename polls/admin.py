from django.contrib import admin
from .models import Poll, Question, AnswerOption, Response


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(Response)
