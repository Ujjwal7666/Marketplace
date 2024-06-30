
from django.urls import path
from .views import detail
from . import views

urlpatterns = [
    path('detail/<pk>',detail, name='detail-pk'),
    path('add/item/', views.new_item, name='add-item' ),
    path('delete/<pk>',views.delete, name='delete'),
    path('edit/<pk>',views.edit_item, name='edit'),
    path('search/', views.search, name='search'),

    ]
