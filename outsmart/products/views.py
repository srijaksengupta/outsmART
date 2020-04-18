from django.shortcuts import render
from .models import ProductPost, Order, OrderItem, Transaction
from .models import Wishlist
from .forms import ProductPostForm, OrderItemForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from .extras import generate_order_id
from django.conf import settings
import datetime
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView

# Stripe related imports
import stripe
from stripe import error
stripe.api_key = settings.STRIPE_SECRET_KEY

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
    order_item, status = OrderItem.objects.get_or_create(product=product, is_ordered=False)
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


@login_required()
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    amount = existing_order.get_cart_total_plus_tax_plus_shipping() * 100
    context = {
        'order': existing_order,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'amount': amount
    }
    return render(request, 'products/checkout.html', context)


@login_required
def charge(request):
    existing_order = get_user_pending_order(request)
    token = request.POST.get('stripeToken', False)
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=int(100 * existing_order.get_cart_total_plus_tax_plus_shipping()),
                currency='inr',
                description='Product charge',
                source=request.POST['stripeToken'],
            )
            messages.success(request, 'Payment was successful')
            return redirect(reverse('products:update_records', kwargs={'token': token}))
            # return redirect('products:browse')
        except stripe.error.CardError as e:
            messages.error(request, e)
    context = {
        'order': existing_order,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'products:charge', context)


@login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    for item in order_items:
        order_item_product = item.product
        order_item_product.stock -= item.quantity
        order_item_product.save()

    # create a transaction
    transaction = Transaction(owner=request.user,
                              token=token,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total_plus_tax_plus_shipping(),
                              success=True)
    # save the transaction (otherwise doesn't exist)
    transaction.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.success(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('products:browse'))


@login_required
def my_wishlist(request):
    context = {'products': Wishlist.objects.filter(owner=request.user)}
    return render(request,'products/wishlist.html',context)


def add_wishlist(request):
    if request.method == 'POST':
        productID = request.POST['product']
        productAdd = ProductPost.objects.get(pk=productID)

        if Wishlist.objects.filter(owner=request.user,product=productAdd).count() == 0:
            p = Wishlist(owner=request.user, product=productAdd)
            p.save()
        return HttpResponse('')
