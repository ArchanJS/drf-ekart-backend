"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apis import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/create/',views.CreateUser.as_view(),name='create_user'),
    path('user/verify/',views.verifyUser,name='verify_user'),
    path('token/obtain/', views.EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/changepassword/', views.changePassword, name='change_password'),
    path('user/getuid/', views.getUid, name='get_uid'),
    path('user/resetpassword/', views.resetPassword, name='reset_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:pk>/', views.GetOrUpdateUser.as_view(), name='get_or_update'),
    path('product/create/', views.CreateProduct.as_view(), name='create_product'),
    path('product/get/', views.GetProducts.as_view(), name='get_products'),
    path('product/get/<int:pk>/', views.GetAProduct.as_view(), name='get_a_product'),
    path('product/buy/', views.buyProduct, name='buy_a_product'),
]
