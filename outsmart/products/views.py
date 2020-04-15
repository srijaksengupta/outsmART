from django.shortcuts import render
from .models import ProductPost
from .models import Wishlist
from .forms import ProductPostForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

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

@login_required
def my_listings(request):
    context = {'products': ProductPost.objects.filter(owner=request.user)}
    return render(request, 'products/listings.html',context)

# Create your views here.
def detail(request, product_id):
    try:
        product = ProductPost.objects.get(pk=product_id)
    except ProductPost.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request,'products/detail.html',{'product': product})


@login_required
def my_wishlist(request):
    context = {'products': Wishlist.objects.filter(owner=request.user)}
    return render(request,'products/wishlist.html',context)

@login_required
def my_cart(request):
    return render(request, 'products/cart.html')


def add_wishlist(request):
    if(request.method) == 'POST':
        productID = request.POST['product']
        productAdd =  ProductPost.objects.get(pk=productID)
        p = Wishlist(owner=request.user, product=productAdd)
        p.save()
        return HttpResponse('')