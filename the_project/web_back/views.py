from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,Http404,FileResponse
from django.contrib.auth import authenticate
from django.db import connection
from django.db.models import Max,Count,Sum
from PIL import Image
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string

import datetime
import base64
import random

# Create your views here.
############################################ 로그인 관련
class user_regist(APIView):     #회원가입
    def post(self,request):
        data_table = UserData()     #유저 테이블에 접근 및 가르키는 레퍼런스
        try:
            chk = UserData.objects.all()        #유저 테이블의 모든 객체를 가져옴
            if chk.filter(user_id = request.data.get("id")).exists():               #아이디 중복 체크
                return JsonResponse({'chk_message':'아이디 중복입니다.'},status=200)
            if chk.filter(user_name = request.data.get("nickname")).exists():       #닉네임 중복체크
                return JsonResponse({'chk_message':'닉네임 중복입니다.'},status=200)
            if chk.filter(user_email = request.data.get("email")).exists():       #닉네임 중복체크
                return JsonResponse({'chk_message':'이메일 중복입니다.'},status=200)
            else:       #모든 중복 체크 통과시
                data_table.user_id = request.data.get("id")             #아이디 저장
                data_table.user_pass = request.data.get("pw")           #비밀번호 저장
                data_table.user_name = request.data.get("nickname")     #닉네임 저장
                data_table.user_email = request.data.get("email")

                data_table.user_comment = '아직 소개말이 입력되지 않았습니다.'
                data_table.user_admin = '0'     #관리자 여부
                data_table.login_state = '0'    #접속 여부
                data_table.user_point = '10'
                data_table.save()               #입력된 데이터 저장

                return JsonResponse({'reg_message':'회원가입 성공!'},status=200)
        except:     #코드 실행중 문제 상황 발생시
           return JsonResponse({'reg_message':'기술적 문제가 발생하여 회원가입에 실패했습니다.'},status=200)


class id_chk(APIView):      #아이디 중복 체크
    def post(self,request):
        chk = UserData.objects.all()        #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user_id = request.data.get("id")).exists():       #아이디 중복시
            return JsonResponse({'chk_message':'아이디 중복입니다.'},status=200)
        else:
            return JsonResponse({'chk_message':'사용 가능한 아이디입니다.'},status=200)


class user_login(APIView):      #로그인
    def post(self,request):
        user_id = request.data.get("id")        #아이디 가져오기
        user_pass = request.data.get("pw")      #비번 가져오기
        chk = UserData.objects.all()            #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user_id = user_id).exists():  #아이디가 존재 할 경우
            pass_test = chk.filter(user_id = user_id).values('user_pass')
            if pass_test.filter(user_pass = user_pass).exists():    #그리고, 그 아이디에 해당하는 비밀번호가 존재 할 경우
                nickname = list(chk.filter(user_id = user_id).values('user_name'))      #로그인 시 닉네임이 필요하다고 하여, 데이터베이스에서 로그인을 요청한 아이디의 닉네임을 가져옴
                return JsonResponse({'login_message': '환영합니다!','return_name':nickname},status=200)  #로그인 완료 메세지와 닉네임에 대한 데이터를 반환
            else:   #비밀번호 실수
                return JsonResponse({'login_message':'비밀번호가 틀렸습니다.'},status=200)
        else:       #아이디 실수
            return JsonResponse({'login_message':'아이디가 틀렸습니다.'},status=200)


############################################ 마이페이지 관련
 

class name_change(APIView):      #닉네임 변경
    def post(self,request):
        if len(request.data.get("nickname")) >= 50:
            return JsonResponse({'chk_message':'닉네임이 너무 깁니다!'},status=200)
        chk = UserData.objects.all()        #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user_name = request.data.get("nickname")).exists():       #닉네임 중복체크
            return JsonResponse({'chk_message':'닉네임 중복입니다.'},status=200)
        change_name = UserData.objects.get(user_id = request.data.get("id") )
        change_name.user_name = request.data.get("nickname")
        change_name.save()
        return JsonResponse({'chk_message':'닉네임이 변경되었습니다.'},status=200)


class pass_change(APIView):      #비밀번호 변경
    def post(self,request):
        chk = UserData.objects.all()        #유저 테이블의 모든 객체를 가져옴
        old_pass = chk.filter(user_id = request.data.get("id")).values('user_pass')
        if old_pass.filter(user_pass = request.data.get("old_pw")).exists():    #그리고, 그 아이디에 해당하는 비밀번호가 존재 할 경우
            change_pass = UserData.objects.get(user_id = request.data.get("id") )
            change_pass.user_pass = request.data.get("new_pw")
            change_pass.save()
            return JsonResponse({'chk_message':'비밀번호가 변경되었습니다.'},status=200)
        else:
            return JsonResponse({'chk_message':'비밀번호가 틀렸습니다.'},status=200)


class email_change(APIView):      #이메일 변경(기존 닉네임 변경에서 코드만 살짝 수정함.)
    def post(self,request):
        chk = UserData.objects.all()        #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user_name = request.data.get("email")).exists():       #이메일 중복체크
            return JsonResponse({'chk_message':'이메일 중복입니다.'},status=200)
        change_email = UserData.objects.get(user_id = request.data.get("id") )
        change_email.user_email = request.data.get("email")
        change_email.save()
        return JsonResponse({'chk_message':'이메일이 변경되었습니다.'},status=200)


class user_comment_change(APIView):      #코맨트 변경(기존 닉네임 변경에서 코드만 살짝 수정함.)
    def post(self,request):
        change_comment = UserData.objects.get(user_id = request.data.get("id"))
        change_comment.user_comment = request.data.get("comment")
        change_comment.save()
        return JsonResponse({'chk_message':'코맨트가 변경되었습니다.'},status=200)

    
class into_mypage(APIView):      #비밀번호 변경
    def post(self,request):
        cursor = connection.cursor()
        #장고의 데이터베이스 연결 방식에서 파이썬 특유의 데이터베이스 연결 방식으로 코드를 바꿔봄.
        #예전에 작성한 코드들의 경우 orm에 대한 숙련도가 없어서 sql문 사용했고, 최근 코드의 경우 orm으로 입출력함
        sql_statement1 = "select user_email, user_comment, user_point from user_data where user_id ='" + request.data.get("id") + "';"       #입력한 아이디값에 맞는 이메일과 소개문을 반환
        result1 = cursor.execute(sql_statement1)      #코드 실행
        data1 = cursor.fetchall()                   #실행 결과 입력

        count_data = [] #카운팅 한 것들
        data_1 = [] #게시글 카운팅
        data_2 = [] #댓글 카운팅

        #작성한 팀 포스트의 갯수와 일반 포스트에 대한 갯수
        team_post_count = TeamPost.objects.filter(user = request.data.get("id")).annotate(Count('post_id')).aggregate(Count('post_id'))
        post_count = PostData.objects.filter(user = request.data.get("id")).annotate(Count('post_id')).aggregate(Count('post_id'))
        total_post_count = team_post_count['post_id__count'] + post_count['post_id__count'] #를 여기에 넣음
        data_1.append(total_post_count)
        #작성한 댓글 수
        comment_sql = CommentData.objects.filter(user = request.data.get("id")).annotate(Count('comment_id')).aggregate(Count('comment_id'))
        data_2.append(comment_sql['comment_id__count'])
        #포스트 수와 댓글 수 합치기
        count_data.append(data_1[0])
        count_data.append(data_2[0])
        #여기서부터는 회원이 가입한 팀의 목록에 대한 것들
        data2 = []

        sql_statement2 = "select team_name from team_user_data where user_id = '" + request.data.get("id") + "' order by team_name;"  #해당 유저가 속한 팀의 리스트를 보여주는 코드.
        result2 = cursor.execute(sql_statement2)      #코드 실행
        in_team = cursor.fetchall()                   #실행 결과 입력

        sql_statement3 = "select team_name, count(*) from team_user_data group by team_name"        #팀별 인원을 보여주는 쿼리문
        result3 = cursor.execute(sql_statement3)            #코드 실행
        num_of_mem = cursor.fetchall()                      #실행 결과 입력

        for i in in_team:
            for j in num_of_mem:
                if i[0] == j[0]:    #i는 회원이 가입한 팀 / j는 모든 팀의 팀원 수 > j의 팀명이 i가 가입한 팀명과 일치시, 리스트에 데이터 추가
                    data2.append(j)
         
        #프로필 사진 관련
        profile_sql = "select user_photo from web_back_profile_photo where user_id = '" + request.data.get("id") + "';"
        profile_result = cursor.execute(profile_sql)      #코드 실행
        profile_data = cursor.fetchall()                   #실행 결과 입력
        if len(profile_data) == 0:
            photo_url = "../the_project/media/media/profile/default.jpg"
        else:
            photo_url = "../the_project/media/media/profile/" + profile_data[0][0]

        with open(photo_url,'rb') as img:
            photo_base64 = base64.b64encode(img.read()).decode('utf-8')

        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제

        return JsonResponse({'user_data':data1,'team_data':data2,'count_data':count_data,'post_data':photo_base64})


class list_of_my_post(APIView):         #내가 쓴 게시글에 대한 목록(팀 게시글, 공용 게시글)
    def post(self,request):
        cursor = connection.cursor()
        list_sql = "select post_id, post_title, team_name 분류, post_time from team_post where user_id = '" + request.data.get("id") + "' union select post_id, post_title, category 분류, post_time from post_data where user_id = '" + request.data.get("id") + "' order by post_time desc;"
        result2 = cursor.execute(list_sql)
        data_list = cursor.fetchall()
        return JsonResponse({'post_list':data_list})


class list_of_my_comment(APIView):      #내가 쓴 댓글에 대하 목록
    def post(self,request):
        cursor = connection.cursor()
        list_sql = "select a.post_id, a.post_title, b.comment_cont, b.comment_id, a.category from post_data a ,comment_data b where a.post_id = b.post_id and b.user_id = '" + request.data.get("id") + "' order by comment_id;"
        result2 = cursor.execute(list_sql)
        data_list = cursor.fetchall()
        return JsonResponse({'post_list':data_list})


class Withdrawal(APIView):          #회원 탈퇴
    def post(self,request):
        try:            #팀장인 경우 / 해당 팀관련 데이터 삭제
            team_maker_data = TeamData.objects.filter(user = request.data.get("id")).values('team_name')    #프론트에서 쏴준 아이디가 만든 팀 리스트 생성
            for i in team_maker_data:           #팀 리스트 하나하나 돌리기
                user_data = TeamUserData.objects.filter(team_name = i['team_name'], is_admin = 0).values('user')    #해당 팀의 비 관리자 회원들에 대한 목록 받기
                for i in user_data: #팀원 한명 한명 체크
                    comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
                    receiver_user = UserData.objects.filter(user_id = i['user']).values('user_id')  #해당 게시글에 대한 정보 불러오기
                    comment_message.receiver_id = UserData.objects.get(pk = receiver_user[0]['user_id']) #쪽지를 받는 사람 아이디 저장
                    comment_message.title = "팀이 삭제되었습니다."                     #이후 데이터 저장
                    comment_message.contents = "'" + team_maker_data + "'팀이 삭제됨에 따라 팀에서 추방되었습니다."  #알림 내용
                    comment_message.category = "fire_team"                                    #알림 종류
                    comment_message.receive_time = datetime.datetime.now()                      #알림 시각
                    comment_message.about_chk = '1'
                    comment_message.save()

                team_user_data = TeamUserData.objects.filter(team_name = i['team_name']) #팀원 삭제
                team_user_data.delete()
                team_post_data = TeamPost.objects.filter(team_name = i['team_name']) #팀 게시글 삭제
                team_post_data.delete()
                team_apply_data = TeamApplyLog.objects.filter(team_name = i['team_name'])    #팀 신청  로그 삭제
                team_apply_data.delete()
                team_chat_data = ChatData.objects.filter(team_name = i['team_name'])     #채팅데이터 삭제
                team_chat_data.delete()
                team_data = TeamData.objects.filter(team_name = i['team_name'])      #팀삭제
                team_data.delete()
        finally:
            team_chat_data = ChatData.objects.filter(user_name = request.data.get("nickname"))  #채팅 작성자 변경
            if bool(team_chat_data):
                team_chat_data.delete()
            team_post_data = TeamPost.objects.filter(user = request.data.get("id"))             #팀 게시글 작성자 변경
            if bool(team_post_data):
                team_post_data.delete()
            user_team_datas = TeamUserData.objects.filter(user = request.data.get("id"))        #소속팀에서 탈퇴
            if bool(user_team_datas):
                user_team_datas.delete()
            user_post_data = PostData.objects.filter(user = request.data.get("id"))             #포스트 작성자 변경
            if bool(user_post_data):
                user_post_data.update(user = 'plz_dont_login_this_account_로그인_하지_마세욨!')
            user_comment_data = CommentData.objects.filter(user = request.data.get("id"))       #댓글 작성자 변경
            if bool(user_comment_data):
                user_comment_data.update(user = 'plz_dont_login_this_account_로그인_하지_마세욨!')
            message_box_data = Message.objects.filter(receiver_id = request.data.get("id"))     #알림 삭제
            if bool(message_box_data):
                message_box_data.delete()   
            apply_log_data = TeamApplyLog.objects.filter(user = request.data.get("id"))         #팀 신청기록 삭제
            if bool(apply_log_data):
                apply_log_data.delete()
            profile_data = WebBackProfilePhoto.objects.filter(user = request.data.get("id"))    #프로필  사진 삭제
            if bool(profile_data):
                profile_data.delete()
            user_data = UserData.objects.filter(user_id = request.data.get("id"))   #최종적으로 해당 회원 삭제
            user_data.delete()
            return JsonResponse({'return_data':'회원탈퇴가 완료 되었습니다!'})
        
class item_list(APIView):      #아이탬 소지 목록
    def post(self,request):
        user_have_item_list = UserItemLog.objects.filter(user_id = request.data.get("id")).values('item_id').order_by('item_id')
        data_list = []
        for i in user_have_item_list:
            data_list.append(i['item_id'])
        return JsonResponse({'item_list':data_list})

############################################ 팀 관련


class make_a_team(APIView):      #팀 생성
    def post(self,request):
        chk = TeamData.objects.all()
        if chk.filter(team_name = request.data.get("teamname")).exists():       #팀이름 중복체크
            return JsonResponse({'chk_message':'팀 이름이 중복입니다.'},status=200)
        #팀명을 사용 할 수 없는 특수 경우
        if request.data.get("teamname") == 'Question' or request.data.get("teamname") == 'Share' or request.data.get("teamname") == 'Team' or request.data.get("teamname") == 'list-group-item':
            return JsonResponse({'chk_message':'사용 할 수 없는 팀 이름입니다.'},status=200)
        #팀 기본 정보
        team_data = TeamData()
        team_data.team_name = request.data.get("teamname")                      #팀명
        team_data.user = UserData.objects.get(pk = request.data.get("id"))      #팀장 아이디
        team_data.introduction = request.data.get("teamdesc")                   #팀 소개
        team_data.team_category = request.data.get("teamcategory")              #팀 카테고리
        
        team_data.team_make_time = datetime.datetime.now()                      #생성한 년 월 일에 대한 정보
        team_data.save()
        #팀원 정보
        team_user_data = TeamUserData()
        team_user_data.user = UserData.objects.get(pk = request.data.get("id"))                 #유저 이름
        team_user_data.team_name = TeamData.objects.get(pk = request.data.get("teamname"))      #팀명
        
        team_user_data.is_admin = '1'
        team_user_data.save()
        #팀 생성시 포인트를 주기 위한 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) + 10
        user_data.save()
        
        return JsonResponse({'chk_message':'팀 생성이 완료되었습니다.'})


class mypage_team_member_list(APIView):             #팀원에 대한 정보(이름, 팀장 여부)를 보여줌 / 마이페이지에서 팀 선택시 팀원 목록 보여줌
    def post(self,request):
        cursor = connection.cursor()
        sql_statement1 = "select user_name, is_admin, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id  and team_name = '" + request.data.get("teamname") + "' order by is_admin desc;"
        #해당 팀에 속한 팀원들 이름과 팀장 여부를 출력하는 쿼리문
        result1 = cursor.execute(sql_statement1)      #코드 실행
        data1 = cursor.fetchall()                   #실행 결과 입력
        #프로필 사진 보여주기 위한 부분.
        photo_64 = []
        for i in data1:
            if i[2] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[2]
            with open(photo_url,'rb') as img:
                photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            photo_64.append(photo_base64)

        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제

        return JsonResponse({'user_data':data1,'photo_data':photo_64})


class team_list2(APIView):              #팀명 / 타임스탬프 / 팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def post(self,request):
        result_list = []
        big_photo_list = []
        cursor = connection.cursor()

        sql_statement1 = "select a.team_name, DATE_FORMAT(a.team_make_time,'%Y/%m/%d'), team_category from team_data a, team_user_data b where a.team_name = b.team_name and b.user_id = '" + request.data.get("id") + "';"
        #팀명과 타임스탬프
        result = cursor.execute(sql_statement1)      #코드 실행
        team_data = cursor.fetchall()                #실행 결과 입력
        for i in team_data:
            small_user_list = []
            small_photo_list = []
            team_user_sql = "select user_name, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id and team_name = '" + i[0] + "';"
            #해당 팀에 속한 팀원을 보여줌
            result = cursor.execute(team_user_sql)      #코드 실행
            team_user_data = cursor.fetchall()          #실행 결과 입력
            small_user_list.append(i)                #팀명과 타임스탬프
            small_user_list.append(team_user_data)   #해당 팀의 팀원
            result_list.append(small_user_list)      #팀명 및 타임스탬프, 팀원 데이터를 뭉친걸 결과 리스트에 담기

            for i in team_user_data:                #한 팀에 대한 사진들을
                if i[1] is None:
                    photo_url = "../the_project/media/media/profile/default.jpg"
                else:
                    photo_url = "../the_project/media/media/profile/" + i[1]

                with open(photo_url,'rb') as img:
                    team_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
                small_photo_list.append(team_photo_base64)  #작은 사진 리스트에 담음
            big_photo_list.append(small_photo_list)         #그리고, 다음팀으로 넘어가기 전 해당 팀에 대한 사진 값을 큰 사진 리스트로 옮김

        return JsonResponse({'user_data':result_list,'photo_data':big_photo_list})
        #팀에 대한 정보(팀명, 타임스탬프)와 팀원에 대한 정보를 함께 전달해주기 위해 for문을 사용함.

        


class team_list3(APIView):              #타임스탬프 / 팀소개 / 팀카테고리 / 팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def post(self,request):
        data_list = []
        cursor = connection.cursor()
        #팀 소개
        sql_statement1 = "select introduction,DATE_FORMAT(team_make_time,'%Y/%m/%d'),team_category from team_data where team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement1)     
        team_data = cursor.fetchall()       
        data_list.append(team_data)
        #팀원 데이터
        sql_statement3 = "select user_name, user_email, user_comment, is_admin, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id and team_name = '" + request.data.get("teamname") + "' order by is_admin desc;"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()
        #팀원들 프로필 사진
        team_photo_64 = []
        for i in user_data:
            if i[4] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[4]
            with open(photo_url,'rb') as img:
                team_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            team_photo_64.append(team_photo_base64)
        #팀 신청 데이터
        sql_statement = "select user_name, user_email, user_comment, user_photo from team_apply_log, user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_apply_log.user_id = user_data.user_id  and team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        #신청자들 프로필 사진
        apply_photo_64 = []
        for i in result_data:
            if i[3] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[3]
            with open(photo_url,'rb') as img:
                apply_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            apply_photo_64.append(apply_photo_base64)

        return JsonResponse({'team_data':data_list,'user_datas':user_data,'apply_list':result_data,'team_photo':team_photo_64,'apply_photo':apply_photo_64})


class team_page(APIView):              #타임스탬프 / 팀소개 / 팀카테고리 / 팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def get(self,request,teamname, format=None):
        data_list = []
        cursor = connection.cursor()
        #팀 소개
        sql_statement1 = "select introduction,DATE_FORMAT(team_make_time,'%Y/%m/%d'),team_category from team_data where team_name = '" + teamname + "';"
        result = cursor.execute(sql_statement1)     
        team_data = cursor.fetchall()       
        data_list.append(team_data)
        #팀원 데이터
        sql_statement3 = "select user_name, user_email, user_comment, is_admin, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id and team_name = '" + teamname + "' order by is_admin desc;"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()
        #팀원들 프로필 사진
        team_photo_64 = []
        for i in user_data:
            if i[4] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[4]
            with open(photo_url,'rb') as img:
                team_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            team_photo_64.append(team_photo_base64)
        #팀 신청 데이터
        sql_statement = "select user_name, user_email, user_comment, user_photo from team_apply_log, user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_apply_log.user_id = user_data.user_id  and team_name = '" + teamname + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        #신청자들 프로필 사진
        apply_photo_64 = []
        for i in result_data:
            if i[3] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[3]
            with open(photo_url,'rb') as img:
                apply_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            apply_photo_64.append(apply_photo_base64)

        return JsonResponse({'team_data':data_list,'user_datas':user_data,'apply_list':result_data,'team_photo':team_photo_64,'apply_photo':apply_photo_64})



class team_authority(APIView):      #팀 정보 페이지 방문 시, 방문자의 권한에 대한 코드
    def post(self,request):
        cursor = connection.cursor()
        sql_statement1 = "select is_admin from team_user_data where user_id = '" + request.data.get("id") + "' and team_name = '" + request.data.get("teamname") + "';"
        #사이트를 접근한 유저의 권한을 알려주는 쿼리문
        result = cursor.execute(sql_statement1)     
        authority = cursor.fetchall()       
        if len(authority) == 0: #만약에 쿼리문이 반환한 값이 없다(즉, 해당 페이지 접근한 사람은 해당 팀 소속이 아니라는 이야기)
            authority = ['-1']  #그래서, 팀 소속이 아니라는것을 알려주는 -1울 넣어주고
            return JsonResponse({'data':authority}) #해당 값을 반환
        return JsonResponse({'data':authority[0]})  #반환 값이 1인 경우 팀장, 0인 경우 팀원


class delete_team_user(APIView):        #팀원 추방
    def post(self,request):
        #팀원 추방 하는 코드
        user_id=UserData.objects.get(user_name=request.data.get("nickname"))
        user = TeamUserData.objects.get(user=user_id,team_name = request.data.get("teamname"))
        user.delete()
        #팀원 추방 후 화면 갱신을 해주기 위해 갱신된 데이터 전송하는 코드
        cursor = connection.cursor()
        sql_statement3 = "select user_name, user_email, user_comment, is_admin, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id and team_name = '" + request.data.get("teamname") + "' order by is_admin desc;"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()
        #갱신된 팀원들 프로필 사진
        team_photo_64 = []
        for i in user_data:
            if i[4] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[4]
            with open(photo_url,'rb') as img:
                team_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            team_photo_64.append(team_photo_base64)
        #알림 보내기
        comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
        user_data_for_message = UserData.objects.get(user_name=request.data.get("nickname"))  #해당 게시글에 대한 정보 불러오기
        id_string1 = str(user_data_for_message.user_id)                                    #게시글을 작성한 유저의 아이디 가져오기
        id_string2 = id_string1.replace('UserData object (', '')            #가져온 값 처리1
        user_id = id_string2.replace(')','')                                #가져온 값 처리2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)
        comment_message.receiver_id = user_id                               #쪽지를 받는 사람 아이디 저장
        comment_message.title = "추방되었습니다."                     #이후 데이터 저장
        comment_message.contents = "'" + request.data.get("teamname") + "'팀에서 추방당하셨습니다."  #알림 내용
        comment_message.category = "fire_team"                                    #알림 종류
        comment_message.receive_time = datetime.datetime.now()                      #알림 시각
        comment_message.about_chk = '1'
        comment_message.save()


        return JsonResponse({'chk_message':'해당 팀원이 추방되었습니다!','datas':user_data,'team_photo':team_photo_64})


class change_team_comment(APIView):     #팀 코맨트 변경
    def post(self,request):
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        team_data.introduction = request.data.get("teamcomment")
        team_data.save()
        return JsonResponse({'chk_message':'팀 코맨트가 수정되었습니다.'})


class team_apply(APIView):          #팀 신청 하는 코드
    def post(self,request):
        #이미 팀 신청을 한 경우
        chk = TeamApplyLog.objects.all()        #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user = request.data.get("id"),team_name = request.data.get("teamname")).exists():
            return JsonResponse({'message':'해당 팀은 이미 신청한 기록이 있습니다!'})
        #만약에 팀에 사람이 8명인 경우
        result_data = TeamUserData.objects.filter(team_name = request.data.get("teamname")).annotate(Count('team_name')).aggregate(Count('team_name'))
        if result_data['team_name__count'] >= 8:
            return JsonResponse({'message':'해당 팀에 현재 남은 자리가 없습니다!'})
        #위의 두 경우에 해당되지 않을 경우
        apply_data = TeamApplyLog()
        apply_data.user = UserData.objects.get(user_id=request.data.get("id"))
        apply_data.team_name = TeamData.objects.get(team_name = request.data.get("teamname"))
        apply_data.save()
        #알림 보내기
        comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
        team_data = TeamData.objects.get(pk = request.data.get("teamname"))  #해당 게시글에 대한 정보 불러오기
        id_string1 = str(team_data.user)                                    #게시글을 작성한 유저의 아이디 가져오기
        id_string2 = id_string1.replace('UserData object (', '')            #가져온 값 처리1
        user_id = id_string2.replace(')','')                                #가져온 값 처리2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)
        comment_message.receiver_id = user_id                               #쪽지를 받는 사람 아이디 저장
        comment_message.title = "팀 신청이 도착했습니다."                     #이후 데이터 저장
        comment_message.contents = "'" + request.data.get("teamname") + "'팀에 대한 신청이 도착했습니다."  #알림 내용
        comment_message.category = "team_apply"                                 #알림 종류
        comment_message.receive_time = datetime.datetime.now()                  #알림 시각
        comment_message.about_chk = '1'
        comment_message.save()

        return JsonResponse({'message':'팀 신청이 완료되었습니다.'})


class team_apply_list(APIView):     #팀 신청 로그 보여주는 코드
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select a.user_name, a.user_email, a.user_comment from user_data a, team_apply_log b where a.user_id = b.user_id and b.team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        return JsonResponse({'apply_list': result_data})


class allow_apply(APIView):
    def post(self,request):
        #신청 로그에서 삭제
        user_data = UserData.objects.get(user_name=request.data.get("nickname"))
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        apply_data = TeamApplyLog.objects.get(user=user_data.user_id,team_name = team_data.team_name)
        apply_data.delete()
        #팀원으로 추가
        user_datas = TeamUserData()
        user_datas.user = UserData.objects.get(user_id= user_data.user_id)
        user_datas.team_name = TeamData.objects.get(team_name = team_data.team_name)
        user_datas.is_admin = 0
        user_datas.save()
        #신청 로그 최신화
        cursor = connection.cursor()
        sql_statement = "select a.user_name, a.user_email, a.user_comment from user_data a, team_apply_log b where a.user_id = b.user_id and b.team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        #갱신된 팀원 데이터
        sql_statement3 = "select user_name, user_email, user_comment, is_admin, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id and team_name = '" + request.data.get("teamname") + "' order by is_admin desc;"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()
        #갱신된 팀원들 프로필 사진
        team_photo_64 = []
        for i in user_data:
            if i[4] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[4]
            with open(photo_url,'rb') as img:
                team_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            team_photo_64.append(team_photo_base64)
        #알림 보내기
        comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
        user_data_for_message = UserData.objects.get(user_name=request.data.get("nickname"))  #해당 게시글에 대한 정보 불러오기
        id_string1 = str(user_data_for_message.user_id)                                    #게시글을 작성한 유저의 아이디 가져오기
        id_string2 = id_string1.replace('UserData object (', '')            #가져온 값 처리1
        user_id = id_string2.replace(')','')                                #가져온 값 처리2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)
        comment_message.receiver_id = user_id                               #쪽지를 받는 사람 아이디 저장
        comment_message.title = "새로운 팀에 가입하였습니다."                     #이후 데이터 저장
        comment_message.contents = "'" + request.data.get("teamname") + "'팀에 대한 신청이 수락되었습니다."  #알림 내용
        comment_message.category = "apply_allow"                                    #알림 종류
        comment_message.receive_time = datetime.datetime.now()                      #알림 시각
        comment_message.about_chk = '1'
        comment_message.save()
        return JsonResponse({'message':'새로운 팀원이 들어왔습니다.','apply_list':result_data,'user_datas':user_data,'team_photo':team_photo_64})

class reject_apply(APIView):        #신청 거절 코드
    def post(self,request):
        user_data = UserData.objects.get(user_name=request.data.get("nickname"))
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        apply_data = TeamApplyLog.objects.get(user=user_data.user_id,team_name = team_data.team_name)
        apply_data.delete()
        #거절 이후 신청 목록 최신화
        cursor = connection.cursor()    
        sql_statement = "select user_name, user_email, user_comment, user_photo from team_apply_log, user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_apply_log.user_id = user_data.user_id  and team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        #신청자들 프로필 사진
        apply_photo_64 = []
        for i in result_data:
            if i[3] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[3]
            with open(photo_url,'rb') as img:
                apply_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            apply_photo_64.append(apply_photo_base64)
        #알림 보내기
        comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
        user_data_for_message = UserData.objects.get(user_name=request.data.get("nickname"))  #해당 게시글에 대한 정보 불러오기
        id_string1 = str(user_data_for_message.user_id)                                    #게시글을 작성한 유저의 아이디 가져오기
        id_string2 = id_string1.replace('UserData object (', '')            #가져온 값 처리1
        user_id = id_string2.replace(')','')                                #가져온 값 처리2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)
        comment_message.receiver_id = user_id                               #쪽지를 받는 사람 아이디 저장
        comment_message.title = "가입 신청이 거절되었습니다."                     #이후 데이터 저장
        comment_message.contents = "'" + request.data.get("teamname") + "'팀에 대한 가입 신청이 거절되었습니다."  #알림 내용
        comment_message.category = "apply_reject"                                    #알림 종류
        comment_message.receive_time = datetime.datetime.now()                      #알림 시각
        comment_message.about_chk = '1'
        comment_message.save()


        return JsonResponse({'message':'신청을 거절했습니다!','apply_list': result_data,'apply_photo':apply_photo_64})


class chat_log(APIView):            #채팅 로그(유니티에서 쏴주는 채팅 로그 데이터를 불러오는 코드)  
    def post(self,request):
        #채팅 로그들
        cursor = connection.cursor()
        sql_statement = "select a.chat_id, a.user_chat, a.user_name, date_format(a.chat_time,'%Y-%m-%d %H:%i') 채팅시간, user_photo from chat_data a, user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where a.user_name = user_data.user_name and a.team_name = '" + request.data.get("teamname") + "' order by chat_id asc;"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        #채팅 로그의 프로필 사진
        profiles_photo_64 = []
        for i in result_data:
            if i[4] is None:
                photo_url = "../the_project/media/media/profile/default.jpg"
            else:
                photo_url = "../the_project/media/media/profile/" + i[4]
            with open(photo_url,'rb') as img:
                apply_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
            profiles_photo_64.append(apply_photo_base64)

        return JsonResponse({'chat_list': result_data,'photo_data':profiles_photo_64})


class search_team(APIView): #검색 기능
    def post(self,request):
        result_list = []
        big_photo_list = []
        cursor = connection.cursor()
        if request.data.get("category") == 'All' and request.data.get("teamname") == "":    #모든 카테고리 + 제목 미입력시 > 모든 게시글 보여주기
            sql_statement = "select team_name, DATE_FORMAT(team_make_time,'%Y/%m/%d'), team_category from team_data order by team_name;"
        elif request.data.get("category") == 'All':     #모든 카테고리, 제목에 특정 단어가 들어간 게시글
            sql_statement = "select team_name, DATE_FORMAT(team_make_time,'%Y/%m/%d'), team_category from team_data where team_name like '%" + request.data.get("teamname") + "%';"
        elif request.data.get("teamname") == "":        #특정 카테고리의 모든 게시글
            sql_statement = "select team_name, DATE_FORMAT(team_make_time,'%Y/%m/%d'), team_category from team_data where team_category like '%" + request.data.get("category") + "%';"
        else:       #특정 카테고리, 제목에 특정 단어가 들어간 게시글
            sql_statement = "select team_name, DATE_FORMAT(team_make_time,'%Y/%m/%d'), team_category from team_data where team_name like '%" + request.data.get("teamname") + "%' and team_category like '%" + request.data.get("category") + "%';"
        
        result = cursor.execute(sql_statement)      #코드 실행
        team_data = cursor.fetchall()               #실행 결과 입력
        for i in team_data:
            small_user_list = []
            small_photo_list = []
            team_user_sql = "select user_name, user_photo from team_user_data,user_data left join web_back_profile_photo on user_data.user_id = web_back_profile_photo.user_id where team_user_data.user_id = user_data.user_id and team_name = '" + i[0] + "';"
            #해당 팀에 속한 팀원을 보여줌
            result = cursor.execute(team_user_sql)      #코드 실행
            team_user_data = cursor.fetchall()          #실행 결과 입력
            small_user_list.append(i)                #팀명과 타임스탬프
            small_user_list.append(team_user_data)   #해당 팀의 팀원
            result_list.append(small_user_list)      #팀명 및 타임스탬프, 팀원 데이터를 뭉친걸 결과 리스트에 담기
            for i in team_user_data:                #한 팀에 대한 사진들을
                if i[1] is None:
                    photo_url = "../the_project/media/media/profile/default.jpg"
                else:
                    photo_url = "../the_project/media/media/profile/" + i[1]
                with open(photo_url,'rb') as img:
                    team_photo_base64 = base64.b64encode(img.read()).decode('utf-8')
                small_photo_list.append(team_photo_base64)  #작은 사진 리스트에 담음
            big_photo_list.append(small_photo_list)         #그리고, 다음팀으로 넘어가기 전 해당 팀에 대한 사진 값을 큰 사진 리스트로 옮김
        return JsonResponse({'team_data':result_list,'photo_data':big_photo_list})


class delete_team(APIView):
    def post(self,request):
        user_data = TeamUserData.objects.filter(team_name =  request.data.get("teamname"), is_admin = 0).values('user')
        for i in user_data:
            comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
            user_data_for_message = UserData.objects.get(user_id = i['user'])  #해당 게시글에 대한 정보 불러오기
            id_string1 = str(user_data_for_message.user_id)                                    #게시글을 작성한 유저의 아이디 가져오기
            id_string2 = id_string1.replace('UserData object (', '')            #가져온 값 처리1
            user_id = id_string2.replace(')','')                                #가져온 값 처리2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)
            comment_message.receiver_id = user_id                               #쪽지를 받는 사람 아이디 저장
            comment_message.title = "팀이 삭제되었습니다."                     #이후 데이터 저장
            comment_message.contents = "'" + request.data.get("teamname") + "'팀이 삭제됨에 따라 팀에서 추방되었습니다."  #알림 내용
            comment_message.category = "fire_team"                                    #알림 종류
            comment_message.receive_time = datetime.datetime.now()                      #알림 시각
            comment_message.about_chk = '1'
            comment_message.save()

        team_user_data = TeamUserData.objects.filter(team_name = request.data.get("teamname")) #팀원 삭제
        team_user_data.delete()
        team_post_data = TeamPost.objects.filter(team_name = request.data.get("teamname")) #팀 게시글 삭제
        team_post_data.delete()
        team_apply_data = TeamApplyLog.objects.filter(team_name = request.data.get("teamname"))    #팀 신청  로그 삭제
        team_apply_data.delete()
        team_chat_data = ChatData.objects.filter(team_name = request.data.get("teamname"))     #채팅데이터 삭제
        team_chat_data.delete()
        team_data = TeamData.objects.filter(team_name = request.data.get("teamname"))      #팀삭제
        team_data.delete()

        return JsonResponse({'return_data':'팀이 삭제되었습니다!'})


class out_team(APIView):
    def post(self,request):
        team_chat_data = ChatData.objects.filter(user_name = request.data.get("nickname"))  #채팅 작성자 삭제
        if bool(team_chat_data):
            team_chat_data.delete()
        team_post_data = TeamPost.objects.filter(user = request.data.get("id"))             #팀 게시글 작성자 삭제
        if bool(team_post_data):
            team_post_data.delete()
        user_data = TeamUserData.objects.filter(team_name =  request.data.get("teamname"), user = request.data.get("id"))
        user_data.delete()      #팀탈퇴
        team_master_id = TeamUserData.objects.filter(team_name =  request.data.get("teamname"), is_admin = 1).values('user')    #팀장 아이디 저장
        team_master_data = Message()
        team_master_data.receiver_id = team_master_id[0]['user']
        team_master_data.title = '팀원 탈퇴'
        team_master_data.contents = request.data.get("id") + '님이 ' + request.data.get("teamname") + '을 탈퇴 했습니다.'
        team_master_data.category = 'teammember_out'
        team_master_data.receive_time = datetime.datetime.now()
        team_master_data.about_chk = 1
        team_master_data.save()
        return JsonResponse({'return_data':'팀에서 탈퇴했습니다!'})



############################################################### 팀게시판 관련


class team_post_list(APIView):      #팀 게시글 목록 보여주는 코드(일반 게시판과 구조가 거의 동일)
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select post_id, post_title, user_name, date_format(post_time,'%Y-%m-%d %H:%i') 시간 from team_post a, user_data b where a.user_id = b.user_id and team_name = '" + request.data.get("teamname") + "' order by a.post_id desc;"
        result = cursor.execute(sql_statement)      #코드 실행
        post_data = cursor.fetchall()               #실행 결과 입력
        return JsonResponse({'post_data': post_data})


class team_post(APIView):       #팀 게시글 코드(일반 게시판과 구조가 거의 동일)
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select post_title, post_contents, date_format(post_time,'%Y-%m-%d %H:%i'), user_name, post_type from team_post a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("id") + "';"
        result = cursor.execute(sql_statement)      #코드 실행
        post_data = cursor.fetchall()               #실행 결과 입력
        if post_data[0][4] == 'file_save':
            sql_statement2 = "select files from web_back_team_file where the_post_id = '" + request.data.get("id") + "';"
            result = cursor.execute(sql_statement2)      #코드 실행
            file_url_result = cursor.fetchall()          #실행 결과 입력

            file_url = str(file_url_result[0])      #url값을 str바꿔주고
            not_processed_file_name = file_url.split('/')        #바꾼 str /를 기준으로 나눠주고
            not_processed_file_name = not_processed_file_name[-1]
            file_name = not_processed_file_name[:-3]
            return JsonResponse({'post_data': post_data,'file_name':file_name})
        else:
            return JsonResponse({'post_data': post_data})


class write_team_post(APIView):         #팀 게시글 작성 코드(일반 게시판과 구조가 거의 동일)
    def post(self,request): 
        post_data = TeamPost()
        post_data.post_title = request.data.get("title")
        post_data.post_contents = request.data.get("contents")
        post_data.post_time = datetime.datetime.now()
        post_data.user = UserData.objects.get(user_id=request.data.get("id"))
        post_data.team_name = TeamData.objects.get(team_name = request.data.get("teamname"))
        post_data.post_type = request.data.get("post_type")
        post_data.save()

        #팀 생성시 포인트를 주기 위한 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) + 2
        user_data.save()

        return JsonResponse({'message': '게시글 작성이 완료되었습니다!'})


class search_team_post(APIView):         #게시글 검색
    def post(self,request):      
        cursor = connection.cursor()
        sql_statement1 = "select post_id, post_title, user_name, date_format(post_time,'%Y-%m-%d %H:%i') 시간 from team_post a, user_data b where a.user_id = b.user_id and team_name = '" + request.data.get("teamname") + "' and post_title like '%" + request.data.get("title")  + "%' order by a.post_id desc;"
        #게시글에 대한 정보를 찾는 쿼리문
        result = cursor.execute(sql_statement1)     
        data = cursor.fetchall()
        return JsonResponse({'post_data':data})


class delete_team_post(APIView):            #팀 게시글 삭제(일반 게시판과 구조가 거의 동일)
    def post(self,request):
        post_data = TeamPost.objects.get(post_id = request.data.get("post_id"))
        post_data.delete()
        return JsonResponse({'chk_message':"게시글이 삭제되었습니다!"})


class modify_team_post_button(APIView):     #팀 게시글 수정하기 버튼( 일반 게시판과 구조가 거의 동일)
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select post_title,post_contents from team_post where post_id = '" + request.data.get("post_id") + "';"
        result = cursor.execute(sql_statement)     
        data = cursor.fetchall()
        
        return JsonResponse({'post_data':data})


class modify_team_post(APIView):            #팀 게시글 수정 완료 버튼(일반 게시판과 구조가 거의 동일)
    def post(self,request):
        post_data = TeamPost.objects.get(pk = request.data.get("post_id"))
        post_data.post_contents = request.data.get("text")
        post_data.post_title = request.data.get("title")
        post_data.save()

        return JsonResponse({'chk_message':"게시글이 수정되었습니다."})


class download_file(APIView):
    queryset = team_file.objects.all()
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = ""

############################################ 게시글 관련


class post_list(APIView):       #게시판 들어갔을때 해당 게시판에 해당되는 글 리스트들 보여주는 코드
    def post(self,request):
        list = []               #게시글 리스트들
        cursor = connection.cursor()
        if request.data.get("order") == "comment":
            sql_statement1 = "select a.post_id, a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, date_format(a.post_time,'%Y-%m-%d %H:%i') 시간, count(c.post_id) 댓글수 from post_data a left join comment_data c on a.post_id = c.post_id, user_data b where a.user_id = b.user_id and category = '" + request.data.get("category") + "' group by a.post_id order by 댓글수 desc;"
        else:
            sql_statement1 = "select a.post_id, a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, date_format(a.post_time,'%Y-%m-%d %H:%i') 시간 from post_data a, user_data b where a.user_id = b.user_id and category = '" + request.data.get("category") + "' order by a." + request.data.get("order")+ ";"
        #게시글의 간략적인 정보들을 가져오는 쿼리문
        result = cursor.execute(sql_statement1)     
        data = cursor.fetchall()
        for i in data:      #해당 게시글의 댓글수를 알려주기 위한 부분
            small_list = []
            sql_statement2 = "select count(*) from comment_data where post_id = " + str(i[0]) + ";" #뎃글수 구하기
            result1 = cursor.execute(sql_statement2)     
            data1 = cursor.fetchall()
            small_list.append(i)
            small_list.append(data1[0])
            list.append(small_list)
        return JsonResponse({'post_data':list})


class the_post(APIView):       #게시글 보는거
    def post(self,request):     
        cursor = connection.cursor()
        sql_statement1 = "select a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, a.contents_data, a.team_name ,date_format(a.post_time,'%Y-%m-%d %H:%i') 시간, a.post_type from post_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("post_id") + "';"
        #게시글 제목, 작성자 이름, 조회수, 추천수, 게시글 내용, 팀 이름(팀 구인 게시판의 경우), 작성날짜를 알려주는 쿼리문
        result1 = cursor.execute(sql_statement1)     
        data1 = cursor.fetchall()
        sql_statement2 = "select a.comment_id, a.comment_cont, b.user_name, date_format(a.comment_time,'%Y-%m-%d %H:%i') 작성시간, a.post_id, a.user_id from comment_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("post_id") +"' order by a.comment_id desc;"
        #해당 게시글에 달려있는 댓글들을 보여주는 쿼리문
        result2 = cursor.execute(sql_statement2)     
        data2 = cursor.fetchall()
        post_data=PostData.objects.get(post_id=request.data.get("post_id"))
        post_data.num_of_open += 1
        post_data.save()
        return JsonResponse({'post_data':data1,'comment_data':data2})


class search_post(APIView):         #게시글 검색
    def post(self,request): 
        list = []                   #게시글 전체 리스트 받아줄 리스트       
        cursor = connection.cursor()
        sql_statement1 = "select a.post_id, a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, date_format(a.post_time,'%Y-%m-%d %H:%i') 시간 from post_data a, user_data b where a.user_id = b.user_id and a.post_title like  '%" + request.data.get("search") + "%' and category = '" + request.data.get("category") + "'order by a.post_id desc;"
        #게시글에 대한 정보를 찾는 쿼리문
        result = cursor.execute(sql_statement1)     
        data = cursor.fetchall()
        for i in data:      #해당 게시글의 댓글수를 알려주기 위한 부분
            small_list = []
            sql_statement2 = "select count(*) from comment_data where post_id = " + str(i[0]) + ";" #게시글 별 댓글 수를 찾는 쿼리문
            result1 = cursor.execute(sql_statement2)     
            data1 = cursor.fetchall()
            small_list.append(i)            #댓글수를 게시글 정보와
            small_list.append(data1[0])     #합침.
            list.append(small_list)         #그리고, 그 정보(게시글 정보와 댓글수)를 list라는 함수에 하나씩 담음
        return JsonResponse({'post_data':list})


class write_post_button(APIView):                                                           #글 작성하러 갈 때 버튼
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select team_name from  team_user_data where user_id = '" + request.data.get("id") + "';"   #팀 리스트 반환
        result = cursor.execute(sql_statement)     
        data = cursor.fetchall()
        return JsonResponse({'team_list':data})


class write_post(APIView):                                                                      #글 작성 완료시 버튼
    def post(self,request):
        post_data = PostData()                                                                  #포스트 테이블
        #게시글 아이디(mysql에서 외래키 지정 이전에 auto_increment 넣는거 깜빡해서 장고에서 처리해줌)
        max_post_id = PostData.objects.all().aggregate(Max('post_id'))
        post_data.post_id = max_post_id['post_id__max'] + 1
        #프론트에서 쏴준 정보들 입력
        post_data.category = request.data.get("category")                                       #카테고리
        if request.data.get("category") == 'Team':                                              #카테고리가 팀인 경우
            post_data.team_name =  TeamData.objects.get(pk = request.data.get("teamname"))      #팀명 입력
        post_data.user = UserData.objects.get(pk = request.data.get("id"))                      #게시자 아이디
        post_data.contents_data = request.data.get("contents")                                  #게시글 내용물
        post_data.post_time = datetime.datetime.now()                                           #게시글 작성 시간
        post_data.post_title = request.data.get("title")                                        #제목
        #mysql의 디폴트 값이 백엔드 부분에서는 사용이 안됨.
        post_data.num_of_open = 0       #조회수
        post_data.num_of_recommend = 0  #추천수
        post_data.save()     

        #팀 생성시 포인트를 주기 위한 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) + 2
        user_data.save()

        return JsonResponse({'post_data':"작성이 완료되었습니다!"})


class recommend_this(APIView):               #추천 기능
    def post(self,request):
        recommend_num = request.data.get("recommendNum")    #해당 게시글의 추천수
        post_data = PostData.objects.get(post_id=request.data.get("boardID"))   #해당 게시글 코드
        post_data.num_of_recommend = recommend_num + 1
        post_data.save()
        cursor = connection.cursor()
        sql_statement = "select a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, a.contents_data, a.team_name ,date_format(a.post_time,'%Y-%m-%d %H:%i') 시간, a.post_type from post_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("boardID") + "';"
        #게시글 제목, 작성자 이름, 조회수, 추천수, 게시글 내용, 팀 이름(팀 구인 게시판의 경우), 작성날짜를 알려주는 쿼리문
        result1 = cursor.execute(sql_statement)     
        data = cursor.fetchall()
        return JsonResponse({'post_data':data})


class post_change(APIView):     #게시글 수정
    def post(self,request):
        post_data = PostData.objects.get(pk = request.data.get("post_id"))      #사용자가 수정하고자하는 게시글의 아이디값에 해당하는 데이터 컬럼
        post_data.contents_data = request.data.get("text")
        post_data.post_title = request.data.get("title")
        if request.data.get("category") == 'Team':      #만약 해당 게시글이 팀 구인이라면
            post_data.team_name = TeamData.objects.get(pk = request.data.get("teamname"))
        post_data.save()
        return JsonResponse({'chk_message':"게시글이 수정되었습니다."})


class post_delete(APIView):     #게시글 삭제
    def post(self,request):
        post_data = PostData.objects.get(post_id = request.data.get("post_id"))
        post_data.delete()
        return JsonResponse({'chk_message':"게시글이 삭제되었습니다!"})


############################################ 데이터 공유


class info_share(APIView):
    def post(self,request):
        post_data = PostData()
        max_post_id = PostData.objects.all().aggregate(Max('post_id'))
        post_data.post_id = max_post_id['post_id__max'] + 1                                     #포스트 id는 AutoIncrement가 안되있어서 넣은 코드
        post_data.user = UserData.objects.get(pk = request.data.get("id"))                      #게시자 아이디
        post_data.contents_data = request.data.get("contents")                                  #게시글 내용물
        post_data.post_time = datetime.datetime.now()                                           #게시글 작성 시간
        post_data.post_title = request.data.get("title")                                        #제목
        post_data.category = request.data.get("category")                                       #카테고리
        post_data.post_type = 'share'                                                           #공유(프론트에서 폼의 차이를 주기 위해)
        post_data.num_of_open = 0       #조회수
        post_data.num_of_recommend = 0  #추천수
        post_data.save()

        #팀 생성시 포인트를 주기 위한 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) + 2
        user_data.save()

        return JsonResponse({'post_data':"작성이 완료되었습니다!"})


class team_share(APIView):          #팀에 게시글 공유(url공유)
    def post(self,request):
        post_data = TeamPost()
        post_data.user = UserData.objects.get(pk = request.data.get("id"))                      #게시자 아이디
        post_data.post_contents = request.data.get("contents")                                  #게시글 내용물
        post_data.post_time = datetime.datetime.now()                                           #게시글 작성 시간
        post_data.post_title = request.data.get("title")                                        #제목
        post_data.team_name = TeamData.objects.get(pk = request.data.get("teamname"))           #공유할 팀 이름                         
        post_data.post_type = 'share'                                                           #공유(프론트에서 폼의 차이를 주기 위해)
        post_data.save()

        #팀 생성시 포인트를 주기 위한 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) + 2
        user_data.save()

        return JsonResponse({'post_data':"작성이 완료되었습니다!"})


############################################ 댓글 관련


class comment_write(APIView):           #코맨트 작성
    def post(self,request):
        comment_data = CommentData()    #댓글 테이블 연결
        comment_data.comment_cont = request.data.get("comment")     #댓글 내용
        comment_data.user = UserData.objects.get(pk = request.data.get("id"))   #댓글 작성자
        comment_data.post = PostData.objects.get(pk = request.data.get("boardID"))  #어느 게시글에 댓글이 달렸는가
        comment_data.comment_time = datetime.datetime.now()         #댓글 작성 시간
        comment_data.save()
        #작성 이후 프론트로 코맨트들 정보 쏴주기
        cursor = connection.cursor()
        sql_statement = "select a.comment_id, a.comment_cont, b.user_name, date_format(a.comment_time,'%Y-%m-%d %H:%i') 작성시간, a.post_id, a.user_id from comment_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("boardID") +"' order by a.comment_id desc;"
        result = cursor.execute(sql_statement)    
        data = cursor.fetchall()
        #알림 보내기
        comment_message = Message()     #쪽지함 관련 테이블(댓글 작성시 게시글 작성자에게 알림이 감)
        post_data = PostData.objects.get(pk = request.data.get("boardID"))  #해당 게시글에 대한 정보 불러오기
        id_string1 = str(post_data.user)                                    #게시글을 작성한 유저의 아이디 가져오기
        id_string2 = id_string1.replace('UserData object (', '')            #가져온 값 처리1
        post_id = id_string2.replace(')','')                                #가져온 값 처리2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)
        #자기가 자기가 쓴 게시글에 댓글을 올린 경우에 대한 예외 처리
        if post_id != request.data.get("id"):
            comment_message.receiver_id = post_id                       #쪽지를 받는 사람 아이디 저장
            title_string1 = str(post_data.post_title)                           #해당 게시글 제목
            title_string2 = title_string1.replace('UserData object (', '')      #값을 처리하는 과정1
            post_id = title_string2.replace(')','')                             #값을 처리하는 과정2(이유는 저장시 값이 UserData object('데이터')로 저장되기 때문)              
            comment_message.title = "'" + post_id + "' 게시글에 댓글이 도착했습니다."   #이후 데이터 저장
            comment_message.contents = request.data.get("comment")              #알림 내용
            comment_message.category = "comment"                                #알림 종류
            comment_message.receive_time = datetime.datetime.now()              #알림 시각
            comment_message.about_chk = '1'
            comment_message.save()

        #팀 생성시 포인트를 주기 위한 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) + 1
        user_data.save()

        return JsonResponse({'comment_data':data})


class comment_delete(APIView):              #댓글 삭제
    def post(self,request):
        comment_data = CommentData.objects.get(comment_id=request.data.get("commentID"))
        comment_data.delete()               #댓글 키값에 맞는 댓글 삭제
        cursor = connection.cursor()
        sql_statement2 = "select a.comment_id, a.comment_cont, b.user_name, date_format(a.comment_time,'%Y-%m-%d %H:%i') 작성시간, a.post_id, a.user_id from comment_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("boardID") +"' order by a.comment_id desc;"
        #해당 게시글에 달려있는 댓글들을 보여주는 쿼리문
        result2 = cursor.execute(sql_statement2)     
        data2 = cursor.fetchall()
        return JsonResponse({'message':"댓글이 삭제되었습니다!",'comment_data':data2})


class comment_change(APIView):              #댓글 수정
    def post(self,request):
        #프론트에서 데이터를 받아서 댓글을 수정하는 부분
        comment_data = CommentData.objects.get(comment_id = request.data.get("commentID"))
        comment_data.comment_cont = request.data.get("comment")
        comment_data.save()
        #이후 갱신된 게시글의 댓글을 다시 쏴주는 부분
        cursor = connection.cursor()
        sql_statement2 = "select a.comment_id, a.comment_cont, b.user_name, date_format(a.comment_time,'%Y-%m-%d %H:%i') 작성시간, a.post_id, a.user_id from comment_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("boardID") +"' order by a.comment_id desc;"
        #해당 게시글에 달려있는 댓글들을 보여주는 쿼리문
        result2 = cursor.execute(sql_statement2)     
        data2 = cursor.fetchall()
        return JsonResponse({'message':"댓글이 수정되었습니다.",'comment_data':data2})


############################################ 파일 업로드 관련


class set_profile(APIView):     #프로필 사진 변경
    def post(self,request):
        image_data = request.FILES['files']     #프론트에서 쏴주는 사진 데이터
        photo_base64 = base64.b64encode(image_data.read()).decode('utf-8')
        try:            #자꾸 외래키 설정 문제로 에러 발생함. 근데 막상 사진 수정은 잘만 됨. 그래서 그냥 어거지로 통과시키는 부분
            user_id = UserData.objects.get(user_id=request.data.get("id"))
            profile_url_data = WebBackProfilePhoto()        #사진 저장 데이터베이스(url부분임) 호출
            profile_url_data.user_photo = image_data        #받은 이미지를 저장하고
            profile_url_data.user = user_id                 #아이디값을 저장(외래키임)
            profile_url_data.save()                         #저장
            profile_data = profile_photo()                  #실제 사진 데이터 저장
            profile_data.user_photo = image_data            #사진 데이터
            profile_data.save()
            return JsonResponse({'message':'프로필 사진 변경 완료!','post_data':photo_base64})
        except:
            return JsonResponse({'message':'프로필 사진 변경 완료!','post_data':photo_base64})


class team_post_file(APIView):     #파일 저장
    def post(self,request):
        #파일 저장을 위해 방금 작성되어 저장된 게시글의 아이디값 가져오기.
        max_post_id = TeamPost.objects.all().aggregate(Max('post_id'))
        #여기부터 파일 저장 부분
        post_file = request.FILES.get('files')
        file_data = team_file()
        file_data.files = post_file
        file_data.the_post_id = max_post_id['post_id__max']     #파일 아이디값과 게시글 아이디값을 맞춰주기 위한 작업
        file_data.save()

        return JsonResponse({'message': '파일 업로드 성공'})


class download_file(APIView):     #파일 다운로드
    queryset = WebBackTeamFile.objects.all()
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select files from web_back_team_file where the_post_id = '" + request.data.get("post_id") + "';"   #해당 게시글에 연류된 파일 다운
        result = cursor.execute(sql_statement)
        data = cursor.fetchall()
        file_url = '../the_project/media/' + data[0][0]

        response = FileResponse(open(file_url, 'rb'))
        response['Content-Disposition'] = 'attachment;filename=' + data[0][0]
        return response


class unity_file(APIView):          #유니티 파일(메타버스 공간 파일 다운로드)
    def get(self, request):
        file_url = '../the_project/media/unity/4.zip'
        response = FileResponse(open(file_url, 'rb'))
        response['Content-Disposition'] = 'attachment;filename=4.zip'
        return response



#쪽지함.
class messege_list(APIView):
    def post(self, request):
        cursor = connection.cursor()
        sql_statement = "select message_id,title,contents,date_format(receive_time,'%Y-%m-%d %H:%i') 알림시간, about_chk from message where receiver_id = '" + request.data.get("id") +"' order by 알림시간;"
        #알람 목록
        result2 = cursor.execute(sql_statement)     
        data2 = cursor.fetchall()
        data_list = []
        for i in data2:
            list_data = list(i)
            data = False
            list_data.append(data)
            data_list.append(list_data)
        message_read = Message.objects.filter(receiver_id = request.data.get("id"))
        message_read.update(about_chk = '0')

        return JsonResponse({'message_list':data_list})



class delete_message(APIView):
    def post(self, request):
        message_data = Message.objects.get(message_id = request.data.get("message_id"))
        message_data.delete()

        cursor = connection.cursor()
        sql_statement = "select message_id,title,contents,date_format(receive_time,'%Y-%m-%d %H:%i') 알림시간 from message where receiver_id = '" + request.data.get("id") +"' order by 알림시간;"
        #알람 목록
        result2 = cursor.execute(sql_statement)     
        data2 = cursor.fetchall()
        data_list = []
        for i in data2:
            list_data = list(i)
            data = False
            list_data.append(data)
            data_list.append(list_data)

        return JsonResponse({'message_list':data_list})


class delete_messages(APIView):
    def post(self, request):
        message_data = Message.objects.filter(receiver_id = request.data.get("id"))     #복사-붙여넣기로 코드들을 참고해서 몰랐는데, get()은 값을 하나만 반환한다...
        message_data.delete()

        return JsonResponse({'message_message':'모든 메세지가 삭제되었습니다!'})


class not_read_message(APIView):
    def post(self,request):
        sum_data = Message.objects.filter(receiver_id=request.data.get("id")).aggregate(Sum('about_chk'))
        if type(sum_data['about_chk__sum']) == int:
            return JsonResponse({'left_message':sum_data['about_chk__sum']})
        return JsonResponse({'left_message':0})



#이메일 관련
class email_send(APIView):     #파일 저장
    def post(self,request):
        rand_num = random.random()
        num = int(rand_num*1000000)
        send_num = str(num).zfill(6)
        recive_email = request.data.get("email")    #수신 이메일
        number = {"number": send_num}       #발신 이메일 html에 값을 넣어주기1
        html_mail = render_to_string("send_email.html", number)    #발신 이메일 html에 값을 넣어주기1
        send_mail(
            'Withrium에서 사용자 이메일 인증을 위해 발송한 메세지입니다.',
            '1',
            'lldp0506@naver.com',
            [recive_email],
            fail_silently=False,
            html_message=html_mail
        )
        return JsonResponse({'sucess_message':send_num})


class find_id(APIView):     #아이디 찾기
    def post(self,request):
        find_id_to_email = request.data.get("email")
        finded_id = UserData.objects.filter(user_email = find_id_to_email).values('user_id')
        if not bool(finded_id):
            return JsonResponse({'id_message':'입력하신 이메일이 맞는 아이디가 없습니다.'})
        return JsonResponse({'id_message':finded_id[0]['user_id']})        


class find_password(APIView):
    def post(self,request):
        id = UserData.objects.filter(user_id = request.data.get("id")).values('user_id')
        email = UserData.objects.filter(user_email = request.data.get("email")).values('user_id')
        try:
            if id[0]['user_id'] == email[0]['user_id']:
                rand_num = random.random()
                num = int(rand_num*1000000)
                send_num = str(num).zfill(6)
                recive_email = request.data.get("email")    #수신 이메일
                number = {"number": send_num}       #발신 이메일 html에 값을 넣어주기1
                html_mail = render_to_string("send_email.html", number)    #발신 이메일 html에 값을 넣어주기1
                send_mail(
                    'Withrium에서 비밀번호 변경에 대한 인증번호입니다.',        #메일 제목
                    '1',                #메일 내용(html파일에 의해 실제로 메일에 표현되지 않음)
                    'lldp0506@naver.com',       #발신인
                    [recive_email],     #수신인
                    fail_silently=False,
                    html_message=html_mail      #html내용
                )
                return JsonResponse({'return_message':send_num})
            else:
                return JsonResponse({'return_message':'입력된 정보 중 아이디 혹은 이메일이 잘못됬습니다.'})
        except:
            return JsonResponse({'return_message':'입력된 정보 중 아이디 혹은 이메일이 잘못됬습니다.'})

class find_password_after_change(APIView):
    def post(self,request):
        old_pass = UserData.objects.filter(user_id = request.data.get("id")).values('user_pass')
        if old_pass[0]['user_pass'] == request.data.get("password"):
            return JsonResponse({'return_message':'새로 입력하신 비밀번호는 기존에 사용하던 것과 같습니다!'})
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_pass = request.data.get("password")
        user_data.save()
        return JsonResponse({'return_message':'비밀번호 수정이 완료 되었습니다!'})
    


############################################ 포인트 상점 관련
#구매 전 포인트 명세서
class before_buy(APIView):
    def post(self,request):
        user_have_point = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        return JsonResponse({'have_point':user_have_point[0]['user_point']})

#아이탬 구매 확정
class buy_item(APIView):
    def post(self,request):
        #아이탬 갖고 있을경우에 대한 부분처리
        chk = UserItemLog.objects.all()
        if chk.filter(user = request.data.get("id"), item_id = request.data.get("item_id")).exists():
            return JsonResponse({'return_message':'이미 보유중인 아이탬입니다!'})
        user_have_point = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')    #갖고 있는 포인트가 부족한 경우
        #이 부분은 프론트단에서 처리해서 주석처리
        #if request.data.get("item_cost") > user_have_point[0]['user_point']:
        #    minus_coin = request.data.get("item_cost") - user_have_point
        #    message = '갖고 계신 포인트가' + minus_coin + '부족합니다!'
        #    return JsonResponse({'return_message':message})
        #구매에 따른 포인트 차감
        left_point = int(user_have_point[0]['user_point']) - int(request.data.get("item_cost"))
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = left_point
        user_data.save()

        #그 밖의 아이탬 구매 로그 추가
        item_data = UserItemLog()
        item_data.user = UserData.objects.get(user_id = request.data.get("id")) #구매한 유저
        item_data.item_id = request.data.get("item_id")
        item_data.item_category = request.data.get("item_category")
        item_data.save()

        return JsonResponse({'return_message':'구매 완료!'})


class buy_randombox(APIView):#가챠 돌린거 결과 저장
    def post(self,request):
        #비용 지불 관련 코드
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        user_data = UserData.objects.get(user_id = request.data.get("id"))
        user_data.user_point = int(old_user_point) - 50
        user_data.save()
        #중복된 아이탬이 가챠 결과로 뜰 경우
        chk = UserItemLog.objects.all()
        if chk.filter(user = request.data.get("id"), item_id = request.data.get("item_id")).exists():
            user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
            old_user_point = user_data[0]['user_point']
            user_data = UserData.objects.get(user_id = request.data.get("id"))
            user_data.user_point = int(old_user_point) + 50
            user_data.save()
            #이후 결과값 전송
            user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
            old_user_point = user_data[0]['user_point']
            return JsonResponse({'return_point':int(old_user_point),'return_message':'이미 보유중인 아이탬입니다!'})
        #가챠 보상이 포인트인경우
        if request.data.get("item_category") == 'Point':
            user_have_point = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
            user_data.user_point = int(user_have_point[0]['user_point']) + int(request.data.get("item_id"))
            user_data.save()
            #이후 결과값 전송
            user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
            old_user_point = user_data[0]['user_point']
            return JsonResponse({'return_point':int(old_user_point)})
        #중복되지 않은 가챠 결과 저장
        item_data = UserItemLog()
        item_data.user = UserData.objects.get(user_id = request.data.get("id")) #구매한 유저
        item_data.item_id = request.data.get("item_id")
        item_data.item_category = request.data.get("item_category")
        item_data.save()
        #이후 결과값 전송
        user_data = UserData.objects.filter(user_id = request.data.get("id")).values('user_point')
        old_user_point = user_data[0]['user_point']
        return JsonResponse({'return_point':int(old_user_point)})