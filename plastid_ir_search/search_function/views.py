from django.shortcuts import render
from .forms import SearchForm


def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search_function/results.html')




    return None