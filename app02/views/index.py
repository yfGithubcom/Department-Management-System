from django.shortcuts import render, redirect


# Create your views here.

# index
def index(request):
    """这是主页"""
    return render(request, 'index.html')
