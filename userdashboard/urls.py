from django.urls import path
from . import views
urlpatterns = [
    path('userdashboard', views.userdashboard, name='userdashboard' ),
    path('dashboarddetail/<pk>', views.dashboarddetail, name='dashboarddetail' ),
]