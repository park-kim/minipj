"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import users
from transactions.views import Transaction
from users.views import Login, Logout, UserManage, UserRegister, VerifyEmail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/register/", UserRegister.as_view(), name="users"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    # Login
    path("users/login/", Login.as_view(), name="login"),
    path("users/logout/", Logout.as_view(), name="logout"),
    path("users/", UserManage.as_view(), name="user_manage"),
    # 이메일 인증
    path("verify/", VerifyEmail.as_view(), name="verify_email"),
    path("transactions/", Transaction.as_view(), name='transactions')
]
