# outsmART

### Introduction to outsmART

outsmART is a web-based marketplace providing a platform to artists so that they can sell their artwork.

In this platform, users (who are can be artists or customers or both) can buy and sell using the same account.

The platform allows any user to upload products to sell, view/modify listing information, delete product listings, track inventory count as items get purchased and view orders that have been made with regards to their listings.

The platform allows users to add products to wish lists, add products to cart (if they are in stock), delete products from cart, update product quantity, check out the product, enter shipping information, make verified payments and view order history.

In order to handle payment verifications, the Stripe API has been integrated with the code.

An integrated chat feature  allows buyers and sellers to chat with each other in real time using a public chat room.

### Assumptions, Constraints and Limitations of outsmART

Our project is almost the perfect fully-functional web application for users to sell and buy artwork. Being the first release, there is always scope for improvement and a few glitches which can be improved on. 

We would like to highlight some of the limitations of outsmART and the constraints and assumptions we have made to handle these limitations:
- Since we are not able to track shipping information which will be handled by a third party, completion of orders on the seller's and buyer's end are not handled.
- Due to this limitation, we put a constraint and assume that a seller must not delete a product from his/her listings if a successful order for it has been made.
- The seller can however update his product stock to 0 after a successful order has been made. 

### Setup

Please do this setup in the following order:

1.	Open the file in your preferred code editor.
2.	Create a virtual env for this project using the command ***pip env shell***
3.	In the terminal, your current directory will be ***/outsmart***.
4.	Now, to install all necessary libraries to support the smooth functioning of this web-based platform, install all packages using the command ***pip install -r requirements.txt***
5.  You must change the directory to outsmart inside the current directory using the command ***cd outsmart/***
6.  On installing all packages successfully and entering the project directory outsmart, make all migrations for the app using the command ***python manage.py makemigrations***
7.	After this, apply all migrations for the app using the command ***python manage.py migrate***
8.	On applying all migrations, you are ready to launch the app on your local server using the command ***python manage.py runserver***

### Created by

Srijak Sengupta & Nadim Rahman