from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.message_list, name='message_list'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/create/', views.message_create, name='message_create'),
    path('message/<int:message_id>/update/', views.message_update, name='message_update'),
    path('message/<int:message_id>/delete/', views.message_delete, name='message_delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('all-messages/', views.all_messages, name='all_messages'),
]

