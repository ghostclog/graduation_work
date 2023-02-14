from django.urls import path

from . import views


urlpatterns = [
    #회원가입 관련
    path('regist/', views.user_regist.as_view() ,name='regist'),    #신청
    path('id_chk/', views.id_chk.as_view() ,name='id_chk'),     #아이디 중복
    path('login/', views.user_login.as_view() ,name='login'),       #로그인

    #마이페이지 관련
    path('mypage/', views.into_mypage.as_view() ,name='mypage'),        #마이페이지
    path('name_ch/', views.name_change.as_view() ,name='name_change'),  #이름 변경
    path('pass_ch/', views.pass_change.as_view() ,name='pass_change'),  #비번 병경
    path('email_ch/', views.email_change.as_view() ,name='mail_change'),    #이메일 변경
    path('comment_ch/', views.user_comment_change.as_view() ,name='comment_change'),    #코맨트 변경
    path('list_of_my_post/', views.list_of_my_post.as_view() ,name='list_of_my_post'),      #내가 쓴 게시글들
    path('list_of_my_comment/', views.list_of_my_comment.as_view() ,name='list_of_my_comment'),     #내가 쓴 코맨트들
    
    #팀 관련(TU는 팀 유저(팀원)을 의미)
    path('make_team/', views.make_a_team.as_view() ,name='make_team'),      #팀 생성
    path('mypage_TUlist/', views.mypage_team_member_list.as_view() ,name='summary_team_list'),  #마이 페이지 팀 요약
    path('detail_team_list/', views.team_list2.as_view() ,name='detail_team_list1'),
    path('detail_team_list2/', views.team_list3.as_view() ,name='detail_team_list2'),       #팀페이지 들어가기 post방식
    path('team_page/<str:teamname>/', views.team_page.as_view() ,name='team_page'),         #팀페이지 들어가기 get방식
    path('team_authority/', views.team_authority.as_view() ,name='team_authority'),         #팀 권한
    path('delete_TU/', views.delete_team_user.as_view() ,name='delete_TU'),             #팀원 강퇴
    path('ch_comment/', views.change_team_comment.as_view() ,name='ch_comment'),        #팀 코맨트 변경
    path('team_apply/', views.team_apply.as_view() ,name='team_apply'),             #팀 신청
    path('allow_apply/', views.allow_apply.as_view() ,name='allow_apply'),          #신청 허락
    path('reject_apply/', views.reject_apply.as_view() ,name='reject_apply'),       #신청 거부
    path('team_apply_list/', views.team_apply_list.as_view() ,name='team_apply_list'),      #신청자 목록
    path('team_chat/', views.chat_log.as_view() ,name='team_chat'),         #팀 채팅
    path('team_search/', views.search_team.as_view() ,name='team_search'),      #팀 검색
    path('delete_team/', views.delete_team.as_view() ,name='team_search'),      #팀 검색

    #팀게시글 관련
    path('team_post_list/', views.team_post_list.as_view() ,name='team_post_list'),     #팀 게시글 목록
    path('team_post/', views.team_post.as_view() ,name='team_post'),            #팀 게시글 보기
    path('search_team_post/', views.search_team_post.as_view() ,name='search_team_post'),       #팀 게시글 검색
    path('write_team_post/', views.write_team_post.as_view() ,name='write_team_post'),      #팀 게시글 작성
    path('write_team_post_with_file/', views.team_post_file.as_view() ,name='file_set'),    #파일을 포함한 팀게시글 작성
    path('delete_team_post/', views.delete_team_post.as_view() ,name='delete_team_post'),   #팀 게시글 삭제
    path('modify_team_post_button/', views.modify_team_post_button.as_view() ,name='modify_team_post_button'),      #팀 게시글 수정하기 버튼
    path('modify_team_post/', views.modify_team_post.as_view() ,name='modify_team_post'),       #팀 게시글 수정 완료 버튼


    #게시글 관련
    path('post_test/', views.post_list.as_view() ,name='post_list'),    #게시글 목록
    path('the_post/', views.the_post.as_view() ,name='the_post'),       #게시글 보기
    path('search_post/', views.search_post.as_view() ,name='search_post'),      #게시글 검색
    path('recommend/', views.recommend_this.as_view() ,name='recommend_this'),      #해당 게시글 추천
    path('post_change/', views.post_change.as_view() ,name='post_change'),      #게시글 수정
    path('post_delete/', views.post_delete.as_view() ,name='comment_delete'),       #게시글 삭제
    path('write_post/', views.write_post.as_view() ,name='write_post'),     #게시글 작성 완료 버튼
    path('write_post_button/', views.write_post_button.as_view() ,name='write_post_button'),        #게시글 작성하기 버튼

    #댓글 관련
    path('write_comment/', views.comment_write.as_view() ,name='write_post'),       #댓글 작성
    path('comment_delete/', views.comment_delete.as_view() ,name='comment_delete'),     #댓글 삭제
    path('comment_change/', views.comment_change.as_view() ,name='comment_change'),     #댓글 수정

    #데이터 곻유
    path('post_info_share/', views.info_share.as_view() ,name='post_info_share'),       #일반 게시글 공유
    path('team_info_share/', views.team_share.as_view() ,name='team_info_share'),       #팀 게시글 공유

    #파일 관련
    path('image_test/', views.set_profile.as_view() ,name='profile_set'),               #프로필 사진 수정
    path('download_file/', views.download_file.as_view() ,name='file_down'),          #파일 다운로드
    path('main_file/', views.unity_file.as_view() ,name='main_down'),                 #유니티 파일

    #쪽지함 관련
    path('messege_list/', views.messege_list.as_view() ,name='letter_box'),         #알림
    path('delete_message/', views.delete_message.as_view() ,name='letter_box'),         #알림
    path('delete_messages/', views.delete_messages.as_view() ,name='letter_box'),         #알림
    path('not_read/', views.not_read_message.as_view() ,name='letter_box'),         #알림
]