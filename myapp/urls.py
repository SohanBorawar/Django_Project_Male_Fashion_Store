from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name='logout'),
    path('about/',views.about,name='about'),
    path('shop/',views.shop,name='shop'),
    path('blog/',views.blog,name='blog'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('forget-password/',views.forget_password,name='forget-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('change-password/',views.change_password,name='change-password'),
    path('category-all/',views.category_all,name='category-all'),
    path('category-clothing/',views.category_clothing,name='category-clothing'),
    path('category-shoes/',views.category_shoes,name='category-shoes'),
    path('category-accessories/',views.category_accessories,name='category-accessories'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('view-details/<int:pk>/',views.view_details,name='view-details'),
    path('shopping-cart/',views.shopping_cart,name='shopping-cart'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),
    path('update-cart/',views.update_cart,name='update-cart'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('success/',views.success,name='success'),
    path('my-orders/',views.my_orders,name='my-orders'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email'),
    path('ajax/validate_oldpassword/',views.validate_changepassword,name='vaildate_oldpassword'),
    path('ajax/validate_cnewpassword/',views.validate_cnewpassword,name ='validate-cnewpassword'),
    path('ajax/validate_Product_title/',views.validate_product_title,name='validate_product_title'),
    path('orders-recieved/',views.orders_recieved,name='orders-recieved'),

    # -------------------------------------------------------------#

    path('seller-registration/',views.seller_registration,name='seller-registration'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('add-product/',views.add_product,name='add-product'),
    path('product-overview/',views.product_overview,name='product-overview'),
    path('view-products/',views.view_products,name='view-products'),
    path('seller-profile/',views.seller_profile,name='seller-profile'),
    path('seller-security/',views.seller_security,name='seller-security'),
    path('seller-view-by-category/',views.seller_view_by_category,name='seller-view-by-category'),
    path('seller-view-single-product/<int:pk>/',views.seller_view_single_product,name='seller-view-single-product'),
    path('edit-product-details/<int:pk>/',views.edit_product_details,name='edit-product-details'),
    path('delete-product/<int:pk>/',views.delete_product,name='delete-product'),
    
]  