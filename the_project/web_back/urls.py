from django.urls import path
from . import views


urlpatterns = [
    path('regist/', views.user_regist.as_view() ,name='regist'),
    path('id_chk/', views.id_chk.as_view() ,name='id_chk'),
    path('login/', views.user_login.as_view() ,name='login'),
    path('name_ch/', views.name_change.as_view() ,name='name_change'),
    path('pass_ch/', views.pass_change.as_view() ,name='name_change'),
]