
from django.urls import path
from  . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('purchase',views.Purchase, name = "purchase"),
    path('checkout/',views.checkout, name = "checkout"),
    path('handlerequest/',views.handlerequest, name="HandleRequest"),
]