from django.shortcuts import render

# Create your views here.

def index(request):
    print("In index")
    return render(request, 'index.html')
