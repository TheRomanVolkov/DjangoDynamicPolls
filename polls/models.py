from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')
    text = models.CharField(max_length=200)
    next_question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_question_options')

    def __str__(self):
        return self.text


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user_id} - {self.question.text}"
