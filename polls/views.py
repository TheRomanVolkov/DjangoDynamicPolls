from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ResponseForm
from .models import Poll, Question, AnswerOption, Response
import uuid

# Главная страница с перечнем опросов
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-start_date')[:5]  # Показать последние 5 опросов
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)


# Пример функции для сохранения ответов пользователя
def save_response(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        # Генерируем уникальный идентификатор для пользователя
        # в реальном проекте реализовал бы сессии или куки
        user_id = str(uuid.uuid4())

        try:
            selected_option = question.answer_options.get(pk=request.POST['answer'])
            new_response = Response(question=question, answer_option=selected_option, user_id=user_id)  # Замените "temporary_user_id" на вашу логику идентификации пользователя
            new_response.save()

            # Проверяем, есть ли следующий вопрос на основе выбранного ответа
            if selected_option.next_question:
                # Если есть следующий вопрос, перенаправляем на него
                return HttpResponseRedirect(reverse('polls:question_view', args=(selected_option.next_question.id,)))
            else:
                # Если следующего вопроса нет, значит, это был последний вопрос опроса
                # Перенаправляем на страницу с результатами опроса
                return HttpResponseRedirect(reverse('polls:results', args=(question.poll.id,)))
        except (KeyError, AnswerOption.DoesNotExist):
            # Обрабатываем ошибку: выбранный ответ не существует или не был выбран
            return render(request, 'polls/question_detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
    else:
        # Если метод не POST, возвращаем пользователя на страницу текущего вопроса
        return redirect('polls:question_view', question_id=question_id)


# Подробное представление опроса с вопросами
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.question_set.all().order_by('order')
    if not questions:
        return render(request, 'polls/no_questions.html', {'poll': poll})
    else:
        first_question = questions[0]
        return redirect('polls:question_view', question_id=first_question.id)


# Представление вопроса с формой для ответа
def question_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST, question_id=question_id)
        if form.is_valid():
            response = form.save(commit=False)
            response.question = question
            response.user_id = str(uuid.uuid4())
            response.save()
            next_question = get_next_question(question, response.answer_option)
            if next_question:
                return redirect('polls:question_view', question_id=next_question.id)
            else:
                return redirect('polls:results', poll_id=question.poll.id)
    else:
        form = ResponseForm(question_id=question_id)
    return render(request, 'polls/question_detail.html', {'question': question, 'form': form})


# Логика для получения следующего вопроса
def get_next_question(current_question, selected_option):
    return selected_option.next_question


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        with connection.cursor() as cursor:
            # Получаем общее количество участников опроса и данные по вопросам и ответам одним запросом
            cursor.execute("""
            SELECT 
                q.id, q.text,
                COUNT(DISTINCT r.user_id) AS responses_count,
                a.text AS answer_text,
                COUNT(r.id) AS answer_count,
                CAST(COUNT(r.id) AS FLOAT) * 100 / (SELECT COUNT(*) FROM polls_response WHERE question_id IN (SELECT id FROM polls_question WHERE poll_id = %s)) AS percentage
            FROM polls_question q
            LEFT JOIN polls_response r ON q.id = r.question_id
            LEFT JOIN polls_answeroption a ON r.answer_option_id = a.id
            WHERE q.poll_id = %s
            GROUP BY q.id, a.id
            ORDER BY responses_count DESC, q.id, a.id
            """, [poll_id, poll_id])

            questions_data = cursor.fetchall()

            current_responses_count = None
            rank = 0
            tie_rank_increment = 1

            questions = {}
            for row in questions_data:
                question_id, question_text, responses_count, answer_text, answer_count, percentage = row

                if question_id not in questions:
                    # Проверяем, нужно ли увеличивать ранг
                    if responses_count != current_responses_count:
                        rank += tie_rank_increment
                        current_responses_count = responses_count
                        tie_rank_increment = 1  # Сбрасываем счетчик повторений ранга
                    else:
                        tie_rank_increment += 1  # Несколько вопросов имеют одинаковое кол-во ответов

                    questions[question_id] = {
                        'rank': rank,
                        'text': question_text,
                        'responses_count': responses_count,
                        'answers': []
                    }
                if answer_text:  # Некоторые вопросы могут не иметь ответов
                    questions[question_id]['answers'].append({
                        'text': answer_text,
                        'count': answer_count,
                        'percentage': percentage
                    })

            context = {
                'poll': poll,
                'questions': list(questions.values())
            }

        return render(request, 'polls/results.html', context)

    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
