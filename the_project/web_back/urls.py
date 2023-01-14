from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    #회원가입 관련
    path('regist/', views.user_regist.as_view() ,name='regist'),
    path('id_chk/', views.id_chk.as_view() ,name='id_chk'),
    path('login/', views.user_login.as_view() ,name='login'),

    #마이페이지 관련
    path('mypage/', views.into_mypage.as_view() ,name='mypage'),
    path('name_ch/', views.name_change.as_view() ,name='name_change'),
    path('pass_ch/', views.pass_change.as_view() ,name='pass_change'),
    path('email_ch/', views.email_change.as_view() ,name='mail_change'),
    path('comment_ch/', views.comment_change.as_view() ,name='comment_change'),
    
    #팀 관련
    path('make_team/', views.make_a_team.as_view() ,name='make_team'),
    path('TU_list/', views.team_list1.as_view() ,name='summary_team_list'),
    path('detail_team_list/', views.team_list2.as_view() ,name='detail_team_list'),
    path('detail_team_list2/', views.team_list3.as_view() ,name='detail_team_list'),
    path('team_authority/', views.team_authority.as_view() ,name='detail_team_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)