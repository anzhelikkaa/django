from django.shortcuts import render
from django.urls import reverse

def index(request):
    links = [
        ('Сторінка 1', reverse('page1')),
        ('Сторінка 2', reverse('page2')),
        ('Сторінка 3', reverse('page3')),
        ('Сторінка 4', reverse('page4')),
    ]
    context = {
        'title': 'Головна сторінка',
        'links': links
    }
    return render(request, 'index.html', context=context)

def page_template(request, name):
    context = {
        'title': name
    }
    return render(request, 'page.html', context=context)

def page1(request):
    return render(request, 'page1.html', {'title': 'Сторінка 1'})

def page2(request):
    return render(request, 'page2.html', {'title': 'Сторінка 2'})

def page3(request):
    return render(request, 'page3.html', {'title': 'Сторінка 3'})

def page4(request):
    return render(request, 'page4.html', {'title': 'Сторінка 4'})
