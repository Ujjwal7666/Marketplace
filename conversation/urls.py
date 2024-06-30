from django.urls import path

from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('new/<pk>', views.new_conversation, name='new'),
    path('conversation/<pk>', views.conversation_detail, name='conversation_detail'),
]
