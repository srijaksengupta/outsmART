from django.shortcuts import render
from .models import ProductPost
from .forms import ProductPostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def browse_products(request):
    context = {'products': ProductPost.objects.all()}
    return render(request,'products/browse.html',context)

@login_required
def add_products(request):
    if request.method == 'POST':
        form = ProductPostForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
    return render(request, 'products/add.html')
