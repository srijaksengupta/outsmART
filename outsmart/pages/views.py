from django.shortcuts import render

# Main homepage view
def index(request):
    return render(request,'pages/index.html')