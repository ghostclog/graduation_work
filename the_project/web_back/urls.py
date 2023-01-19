from django.urls import path

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
    path('comment_ch/', views.user_comment_change.as_view() ,name='comment_change'),
    
    #팀 관련(TU는 팀 유저(팀원)을 의미)
    path('make_team/', views.make_a_team.as_view() ,name='make_team'),
    path('TU_list/', views.team_list1.as_view() ,name='summary_team_list'),
    path('detail_team_list/', views.team_list2.as_view() ,name='detail_team_list1'),
    path('detail_team_list2/', views.team_list3.as_view() ,name='detail_team_list1'),
    path('team_authority/', views.team_authority.as_view() ,name='team_authority'),
    path('delete_TU/', views.delete_team_user.as_view() ,name='delete_TU'),
    path('ch_comment/', views.change_team_comment.as_view() ,name='ch_comment'),
    path('team_apply/', views.team_apply.as_view() ,name='ch_comment'),
    path('allow_apply/', views.allow_apply.as_view() ,name='ch_comment'),
    path('reject_apply/', views.reject_apply.as_view() ,name='ch_comment'),
    path('team_apply_list/', views.team_apply_list.as_view() ,name='ch_comment'),

    #게시글 관련
    path('post_test/', views.post_list.as_view() ,name='post_list'),
    path('the_post/', views.the_post.as_view() ,name='the_post'),
    path('search_post/', views.search_post.as_view() ,name='search_post'),
    path('recommend/', views.recommend_this.as_view() ,name='recommend_this'),
    path('post_change/', views.post_change.as_view() ,name='post_change'),
    path('post_delete/', views.post_delete.as_view() ,name='comment_delete'),
    path('write_post/', views.write_post.as_view() ,name='write_post'),
    path('write_post_button/', views.write_post_button.as_view() ,name='write_post_button'),

    #댓글 관련
    path('write_comment/', views.comment_write.as_view() ,name='write_post'),
    path('comment_delete/', views.comment_delete.as_view() ,name='write_post'),
    path('comment_change/', views.comment_change.as_view() ,name='write_post'),

    #이미지 테스트 관련
    path('image_test/', views.set_profile.as_view() ,name='test1'),
]