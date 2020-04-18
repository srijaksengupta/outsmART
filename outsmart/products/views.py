from django.shortcuts import render
from .models import ProductPost, Order, OrderItem
from .models import Wishlist
from .forms import ProductPostForm, OrderItemForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from .extras import generate_order_id
import datetime
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
            messages.success(request, 'Product added successfully')
            return redirect('products:listings')
        else:
            messages.error(request, 'Product addition failed')
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
                messages.success(request, 'Product updated successfully')
                return redirect('products:listings')

        except Exception as e:
            messages.error(request, 'Product update failed')
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
            messages.success(request, 'Product deleted successfully')
            return redirect('products:listings')
        except Exception as e:
            messages.error(request, 'Product delete failed')
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
def my_cart(request):
    return render(request, 'products/cart.html')

@login_required()
def add_to_cart(request, **kwargs):
    # filter products by id
    product = ProductPost.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product.owner == request.user:
        messages.info(request, 'This is your product listing')
        return redirect('products:browse')
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=request.user, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.success(request, "Item added to cart successfully")
    return redirect('products:browse')


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.success(request, "Item deleted from cart successfully")
    else:
        messages.error(request, 'Failed to delete item from cart')
    return redirect(reverse('products:order_summary'))


def get_user_pending_order(request):
    # get order for the correct user
    order = Order.objects.filter(owner=request.user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'products/cart.html', context)

@login_required
def edit_item(request, item_id):
    template = 'products/edit_item.html'
    item = get_object_or_404(OrderItem, pk=item_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        try:
            if form.is_valid():
                data = form.cleaned_data
                quantity = data['quantity']
                if quantity <= item.product.stock:
                    form.save()
                    messages.success(request, 'Item quantity updated successfully')
                    return redirect('products:order_summary')
                else:
                    messages.error(request, 'The quantity requested for this item is not available')
        except Exception as e:
            messages.error(request, e)
            # messages.error(request, 'Item quantity update failed')
    else:
        form = OrderItemForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return render(request, template, context)


@login_required
def my_wishlist(request):
    context = {'products': Wishlist.objects.filter(owner=request.user)}
    return render(request,'products/wishlist.html',context)


def add_wishlist(request):
    if(request.method) == 'POST':
        productID = request.POST['product']
        productAdd = ProductPost.objects.get(pk=productID)

        if(Wishlist.objects.filter(owner=request.user,product=productAdd).count()==0):
            p = Wishlist(owner=request.user, product=productAdd)
            p.save()
        return HttpResponse('')
