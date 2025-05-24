from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>', views.edit_gender),
    path('gender/delete/<int:genderId>', views.delete_gender),
    path('users/list', views.user_list),
    path('add/user', views.add_user),
    path('edit/user/<int:userId>', views.edit_user),
    path('delete/user/<int:userId>', views.delete_user),
    path('', views.log_in, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('user/password/<int:userId>/', views.password, name='password'),
  
   
]
