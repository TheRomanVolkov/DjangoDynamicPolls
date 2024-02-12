from django.shortcuts import render


def index(request):
    # Логика для отображения главной страницы
    return render(request, 'index.html')
