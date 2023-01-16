from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,Http404
from django.contrib.auth import authenticate
from django.db import connection
import datetime

from rest_framework.views import APIView

from .models import *


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



class comment_change(APIView):      #코맨트 변경(기존 닉네임 변경에서 코드만 살짝 수정함.)
    def post(self,request):
        change_comment = UserData.objects.get(user_id = request.data.get("id") )
        change_comment.user_comment = request.data.get("comment")
        change_comment.save()
        return JsonResponse({'chk_message':'코맨트가 변경되었습니다.'},status=200)


    
class into_mypage(APIView):      #비밀번호 변경
    def post(self,request):
        cursor = connection.cursor()
        #장고의 데이터베이스 연결 방식에서 파이썬 특유의 데이터베이스 연결 방식으로 코드를 바꿔봄.
        #사용해본 결과 데이터 입력 시에는 orm이 편한데. select문에 한해서는 쿼리문이 더편함
        sql_statement1 = "select user_email, user_comment from user_data where user_id ='" + request.data.get("id") + "';"       #입력한 아이디값에 맞는 이메일과 소개문을 반환
        result1 = cursor.execute(sql_statement1)      #코드 실행
        data1 = cursor.fetchall()                   #실행 결과 입력

        data2 = []

        sql_statement2 = "select tema_name from team_user_data where user_id = '" + request.data.get("id") + "';"  #해당 유저가 속한 팀의 리스트를 보여주는 코드.
        result2 = cursor.execute(sql_statement2)      #코드 실행
        in_team = cursor.fetchall()                   #실행 결과 입력

        sql_statement3 = "select tema_name, count(*) from team_user_data group by tema_name"        #팀별 인원을 보여주는 쿼리문
        result3 = cursor.execute(sql_statement3)            #코드 실행
        num_of_mem = cursor.fetchall()                      #실행 결과 입력

        for i in in_team:
            for j in num_of_mem:
                if i[0] == j[0]:
                    data2.append(j)



        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제

        return JsonResponse({'user_data':data1,'team_data':data2})    #data 자체는 튜플형식이나 json으로 보내지는 과정에서 알아서 배열로 바뀌는듯함. 프론트로에서 배열로 값이 왔다고함.



############################################ 팀 관련



class make_a_team(APIView):      #팀 생성
    def post(self,request):
        chk = TeamData.objects.all()
        if chk.filter(team_name = request.data.get("teamname")).exists():       #팀이름 중복체크
            return JsonResponse({'chk_message':'팀 이름이 중복입니다.'},status=200)
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
        team_user_data.tema_name = TeamData.objects.get(pk = request.data.get("teamname"))      #팀명
        
        team_user_data.is_admin = '1'
        team_user_data.save()
        
        return JsonResponse({'chk_message':'팀 생성이 완료되었습니다.'})



class team_list1(APIView):             #팀원에 대한 정보(이름, 팀장 여부)를 보여줌
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select user_id, is_admin from team_user_data where tema_name = '" + request.data.get("teamname") + "' order by is_admin desc;"
        #해당 팀에 속한 팀원들 이름과 팀장 여부를 출력하는 쿼리문
        result = cursor.execute(sql_statement)      #코드 실행
        data = cursor.fetchall()                   #실행 결과 입력

        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제

        return JsonResponse({'user_data':data})


    
class team_list2(APIView):              #팀명 / 타임스탬프 / 팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def post(self,request):
        result_list = []
        cursor = connection.cursor()

        sql_statement1 = "select a.team_name, DATE_FORMAT(a.team_make_time,'%Y/%m/%d') from team_data a, team_user_data b where a.team_name = b.tema_name and b.user_id = '" + request.data.get("id") + "';"
        #팀명과 타임스탬프
        result = cursor.execute(sql_statement1)      #코드 실행
        team_data = cursor.fetchall()                #실행 결과 입력
        for i in team_data:
            small_list = []
            team_user_sql = "select user_name from team_user_data a, user_data b where a.user_id = b.user_id and a.tema_name = '" + i[0] + "';"
            #해당 팀에 속한 팀원을 보여줌
            result = cursor.execute(team_user_sql)      #코드 실행
            team_user_data = cursor.fetchall()          #실행 결과 입력

            small_list.append(i)
            small_list.append(team_user_data)
            result_list.append(small_list)

        return JsonResponse({'user_data':result_list})
        #팀에 대한 정보(팀명, 타임스탬프)와 팀원에 대한 정보를 함께 전달해주기 위해 for문을 사용함.



class team_list3(APIView):              #타임스탬프 / 팀소개 / 팀카테고리 /팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def post(self,request):
        data_list = []
        cursor = connection.cursor()
        sql_statement1 = "select introduction,DATE_FORMAT(team_make_time,'%Y/%m/%d'),team_category from team_data where team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement1)     
        team_data = cursor.fetchall()       
        data_list.append(team_data)

        sql_statement3 = "select a.user_name, a.user_email, a.user_comment, b.is_admin from user_data a, team_user_data b where a.user_id = b.user_id and tema_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()


        return JsonResponse({'team_data':data_list,'user_datas':user_data})
        


class team_authority(APIView):
    def post(self,request):
        cursor = connection.cursor()
        sql_statement1 = "select is_admin from team_user_data where user_id = '" + request.data.get("id") + "' and tema_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement1)     
        authority = cursor.fetchall()       
        if len(authority) == 0:
            authority = ['-1']
            return JsonResponse({'data':authority})
        return JsonResponse({'data':authority[0]})



class delete_team_user(APIView):        #팀원 추방
    def post(self,request):
        user_id=UserData.objects.get(user_name=request.data.get("nickname"))
        user = TeamUserData.objects.get(user=user_id,tema_name = request.data.get("teamname"))
        user.delete()
        #팀원 추방 후 화면 갱신을 
        cursor = connection.cursor()
        sql_statement3 = "select a.user_name, a.user_email, a.user_comment, b.is_admin from user_data a, team_user_data b where a.user_id = b.user_id and tema_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()

        return JsonResponse({'chk_message':'해당 팀원이 추방되었습니다!','datas':user_data})



class change_team_comment(APIView):     #팀 코맨트 변경
    def post(self,request):
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        team_data.introduction = request.data.get("teamcomment")
        team_data.save()
        return JsonResponse({'chk_message':'팀 코맨트가 수정되었습니다.'})



############################################ 게시글 관련


class post_list(APIView):       #게시판 들어갔을때 해당 게시판에 해당되는 글 리스트들 보여주는 코드
    def post(self,request):
        list = []

        cursor = connection.cursor()

        sql_statement1 = "select a.post_id, a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, date_format(a.post_time,'%Y-%m-%d %h:%m') from post_data a, user_data b where a.user_id = b.user_id and category = '" + request.data.get("category") + "';"
        result = cursor.execute(sql_statement1)     
        data = cursor.fetchall()

        for i in data:      #해당 게시글의 댓글수를 알려주기 위한 부분
            small_list = []

            sql_statement2 = "select count(*) from comment_data where post_id = " + str(i[0]) + ";"
            result1 = cursor.execute(sql_statement2)     
            data1 = cursor.fetchall()

            small_list.append(i)
            small_list.append(data1[0])

            list.append(small_list)

        return JsonResponse({'post_data':list})



class the_post(APIView):       #게시글 보는거
    def post(self,request):

        cursor = connection.cursor()
        sql_statement1 = "select a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, a.contents_data ,date_format(a.post_time,'%Y-%m-%d %h:%m') from post_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("post_id") + "';"
        result1 = cursor.execute(sql_statement1)     
        data1 = cursor.fetchall()

        sql_statement2 = "select a.comment_id, a.comment_cont, b.user_name, date_format(a.comment_time,'%Y-%m-%d %h:%m') 작성시간, a.post_id, a.user_id from comment_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("post_id") +"' order by 작성시간;"
        result2 = cursor.execute(sql_statement2)     
        data2 = cursor.fetchall()


        return JsonResponse({'post_data':data1,'comment_data':data2})
############################################ 이미지 관련(테스트중)



class upload_photo(APIView):
    def post(self,request):
        photo_data = Post()
        photo_data.user_id = 'aaaa'
        photo_data.photo = request.FILES['files']
        photo_data.save()

        images = list(Post.objects.all())

        return JsonResponse({'chk_message':images})