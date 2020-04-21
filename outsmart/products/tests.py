from django.test import TestCase
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.test import Client
from .models import ProductPost, OrderItem, Order
from django.contrib.auth.models import User

#Create a user
def create_user(name):
        user = User.objects.create(username=name)
        user.set_password('12345')
        user.save()
        return user

#Log the user
def log_user(self,name):
    return self.client.login(username=name, password='12345')

#Create a default product
def create_product(name,owner,stock,sold,price):
    return ProductPost.objects.create(
        owner=owner, 
        title=name,
        summary="Blah",
        descrip="BlahBlah",
        stock=stock,
        tags="Test",
        image="test",
        price=price,
        sold=sold,
        revenue=0.00)

class OrderModelTests(TestCase):

    # Check if the cart total is calculated correctly
    def test_cart_total_correct(self):
        #creater a buyer and seller
        user1=create_user("User1")
        user2=create_user("User2")

        product1 = create_product("Product1", user2,3,0,3.99)
        product2 = create_product("Product2", user2,3,0,10.99)

        # create order items associated with products
        order_item, status = OrderItem.objects.get_or_create(product=product1, is_ordered=False)
        order_item2, status = OrderItem.objects.get_or_create(product=product2, is_ordered=False)

        # create order associated with the user
        user_order, status = Order.objects.get_or_create(owner=user1, is_ordered=False)
        user_order.items.add(order_item)
        user_order.items.add(order_item2)

        # check if the function that calculates cart total is equal to the manual total
        self.assertEqual(14.98, user_order.get_cart_total())

class ListViewTest(TestCase):

    # Check if a product is in listings
    def test_product_in_listings(self):

        #Create seller
        User3 = create_user("User3")
        #Log seller to access listings page
        logged_in = log_user(self,'User3')
        #Create a product
        product1 = create_product("Product1", User3,3,0,3.99)
        response = self.client.get(reverse('products:listings'))

        #Check if product added to listing
        self.assertQuerysetEqual(
            response.context['products'],
            ['<ProductPost: Product: Product1 by User3>']
        )

class BrowseViewTest(TestCase):
    #Check if browse page has no products if there are no products in database
    def test_browse_no_products(self):
        response = self.client.get(reverse('products:browse'))

        self.assertQuerysetEqual(
            response.context['products'],
            []
        )

    #Check if browse page has no products if one product in database
    def test_browse_one_product(self):
        user1=create_user("User1")
        product1 = create_product("Product1", user1,3,0,3.99)
        response = self.client.get(reverse('products:browse'))

        self.assertQuerysetEqual(
            response.context['products'],
            ['<ProductPost: Product: Product1 by User1>']
        )

    #Check if browse page has multiple products in the database, in the default order
    def test_browse_multiple_products_default(self):
        user1=create_user("User1")

        #product2 has sold more items, so it should be displayed first
        product1 = create_product("Product1", user1,3,0,3.99)
        product2 = create_product("Product2", user1,3,1,3.99)

        response = self.client.get(reverse('products:browse'))

        #display products in the order of items sold
        self.assertQuerysetEqual(
            response.context['products'],
            ['<ProductPost: Product: Product2 by User1>','<ProductPost: Product: Product1 by User1>']
        )