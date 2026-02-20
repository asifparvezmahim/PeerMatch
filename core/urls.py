from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('researchers/', views.researchers, name='researchers'),
    path('idea/new/', views.new_idea, name='new_idea'),
    path('idea/<int:idea_id>/', views.idea_detail, name='idea_detail'),
    path('idea/edit/<int:id>/', views.edit_idea, name='edit_idea'),
    path('idea/delete/<int:id>/', views.delete_idea, name='delete_idea'),
    path('request_collab/<int:idea_id>/', views.request_collab, name='request_collab'),
    path('respond_request/<int:req_id>/<str:status>/', views.respond_request, name='respond_request'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('dashboard/', views.my_profile, name='dashboard'), # redirect alias
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/<int:user_id>/', views.conversation, name='conversation'),
    path('api/messages/send/', views.api_send_message, name='api_send_message'),
    path('api/messages/<int:user_id>/', views.api_messages, name='api_messages'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/block/<int:user_id>/', views.block_user, name='block_user'),
    path('admin/make_admin/<int:user_id>/', views.make_admin, name='make_admin'),
]
