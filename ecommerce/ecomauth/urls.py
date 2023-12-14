
from django.urls import path
from  ecomauth import views


urlpatterns = [
    path('signup/',views.signup, name = 'signup'),
    path('login/',views.handlelogin, name = 'handlelogin'),
    path('logout/',views.handlelogout, name='handlelogout'),
    # path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('activate/(?<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate,name='activate'),
    
]