from django.shortcuts import render
from .models import ProductPost
from .models import Wishlist
from .forms import ProductPostForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView

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
            messages.success(request, 'Product has been successfully added')
            return redirect('products:listings')
    return render(request, 'products/add.html')

@login_required
def my_listings(request):
    context = {'products': ProductPost.objects.filter(owner=request.user)}
    return render(request, 'products/listings.html',context)

@login_required
def edit_products(request, pk):
    template = 'products/modify.html'
    product = get_object_or_404(ProductPost, pk=pk)
    if request.method == 'POST':
        form = ProductPostForm(request.POST, instance=product)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Product has been successfully updated')
                return redirect('products:listings')

        except Exception as e:
            messages.warning(request, 'Product update failed')
    else:
        form = ProductPostForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)

@login_required
def delete_products(request, pk):
    template = 'products/delete.html'
    product = get_object_or_404(ProductPost, pk=pk)
    if request.method == 'POST':
        form = ProductPostForm(request.POST, instance=product)
        try:
            product.delete()
            messages.success(request, 'Product has been successfully deleted')
            return redirect('products:listings')
        except Exception as e:
            messages.warning(request, 'Product delete failed')
    else:
        form = ProductPostForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)

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
        productAdd = ProductPost.objects.get(pk=productID)

        if(Wishlist.objects.filter(owner=request.user,product=productAdd).count()==0):
            p = Wishlist(owner=request.user, product=productAdd)
            p.save()
        return HttpResponse('')