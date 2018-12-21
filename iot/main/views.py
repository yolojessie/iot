from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    '''
    Show 'Hello world!' in the main page
    '''
    context = {}
    return render(request, 'main/main.html', context)

