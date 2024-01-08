"""
URL configuration for new_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from rest_framework.authtoken import views as rest_framework_views

from rest_framework.routers import DefaultRouter
from attendanceportal import views
#from attendanceportal.views import AttendanceView

#router = DefaultRouter()
#router.register(r'CustomUser', AttendanceView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="signin"),
    #path('api-token-auth/', rest_framework_views.obtain_auth_token,name="api-token-auth"),
    path("otp_verification", views.verify_otp, name="otp_verification"),
    path("edit", views.edit_view, name="edit"),
    path("update", views.update_view, name="update"),


]
