from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница приложения polls, список опросов
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),  # Подробная страница опроса, с первым вопросом или сообщением об отсутствии вопросов
    path('question/<int:question_id>/', views.question_view, name='question_view'),  # Представление для отображения вопроса и приема ответа
    path('<int:poll_id>/results/', views.results, name='results'),  # Страница с результатами опроса
    path('response/<int:question_id>/', views.save_response, name='save_response'),
]
