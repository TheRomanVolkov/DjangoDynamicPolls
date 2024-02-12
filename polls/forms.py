from django import forms
from .models import Response, AnswerOption


# Форма для ответа пользователя
class ResponseForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=AnswerOption.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    class Meta:
        model = Response
        fields = ['answer']

    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id', None)
        super(ResponseForm, self).__init__(*args, **kwargs)
        if question_id:
            self.fields['answer'].queryset = AnswerOption.objects.filter(question_id=question_id)
