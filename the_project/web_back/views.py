from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,Http404
from django.contrib.auth import authenticate
from django.db import connection
from django.db.models import Max,Count
from PIL import Image



import datetime
import base64

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

              
                #photo = Image.open("../the_project/media/media/profile/default.jpg")
                #profile_data = Profile()
                #profile_data.user = UserData.objects.get(user_id = request.data.get("id"))
                #photo_base64 = base64.b64encode(photo).decode('utf-8')
                #profile_data.profile_data = photo_base64

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
        #사용해본 결과 데이터 입력 시에는 orm이 편한데. select문에 한해서는 쿼리문이 더편함
        sql_statement1 = "select user_email, user_comment from user_data where user_id ='" + request.data.get("id") + "';"       #입력한 아이디값에 맞는 이메일과 소개문을 반환
        result1 = cursor.execute(sql_statement1)      #코드 실행
        data1 = cursor.fetchall()                   #실행 결과 입력

        data2 = []

        sql_statement2 = "select team_name from team_user_data where user_id = '" + request.data.get("id") + "';"  #해당 유저가 속한 팀의 리스트를 보여주는 코드.
        result2 = cursor.execute(sql_statement2)      #코드 실행
        in_team = cursor.fetchall()                   #실행 결과 입력

        sql_statement3 = "select team_name, count(*) from team_user_data group by team_name"        #팀별 인원을 보여주는 쿼리문
        result3 = cursor.execute(sql_statement3)            #코드 실행
        num_of_mem = cursor.fetchall()                      #실행 결과 입력

        for i in in_team:
            for j in num_of_mem:
                if i[0] == j[0]:
                    data2.append(j)



        
        
        #프로필 사진 관련

        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제

        #profile = Profile.objects.all() 
        #data3 = profile.filter(user = request.data.get("id")).values('profile_data')

        return JsonResponse({'user_data':data1,'team_data':data2})



class set_profile(APIView):     
    def post(self,request):     #기존에 프로필 사진을 저장하는 방식은 프론트에서 사진을 받고 폴더에 저장한 다음 해당 url을 mysql에 저장하는 방식이였음.
                                #그러나, 해당 방식 이용 과정에서 mysql에 2006 문제가 발생했고, 해결을 못하여 결국 base64 데이터를 mysql에 저장하기로함
                                #비효울적이라는건 알고 있으나, 실력 및 경험 부족. 그리고, 피드백 및 조언 해주는 사람을 구하기 어렵다는 독학 특성의 한계로 생각함.. XD
        photo = request.FILES['files']
        photo_base64 = base64.b64encode(photo.read()).decode('utf-8')
        user_id = UserData.objects.get(user_id = request.data.get("id")) 
        profile_data = Profile.objects.get(user_id = user_id)
        profile_data.profile_data = photo_base64
        profile_data.save()

        return JsonResponse({'message':'프로필 사진 변경 완료!','post_data':photo_base64})



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
        team_user_data.team_name = TeamData.objects.get(pk = request.data.get("teamname"))      #팀명
        
        team_user_data.is_admin = '1'
        team_user_data.save()
        
        return JsonResponse({'chk_message':'팀 생성이 완료되었습니다.'})



class team_list1(APIView):             #팀원에 대한 정보(이름, 팀장 여부)를 보여줌
    def post(self,request):
        cursor = connection.cursor()
        sql_statement1 = "select user_id, is_admin from team_user_data where team_name = '" + request.data.get("teamname") + "' order by is_admin desc;"
        #해당 팀에 속한 팀원들 이름과 팀장 여부를 출력하는 쿼리문
        result1 = cursor.execute(sql_statement1)      #코드 실행
        data1 = cursor.fetchall()                   #실행 결과 입력

        sql_statement2 = "select count(*) from team_user_data where team_name = '" + request.data.get("teamname") + "';"
        result2 = cursor.execute(sql_statement2)      #코드 실행
        data2 = cursor.fetchall() 
        
        #count_data = TeamUserData.objects.filter(team_name = request.data.get("teamname")).annotate(Count('team_name')).aggregate(Count('team_name'))
        #incount = count_data['team_name__count']

        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제
        #phot_list = []
        #for i in range(incount):
        #    sql_statement3 = "select photo from web_back_post where user_id = '" + data1[i][0] + "';"
        #    result3 = cursor.execute(sql_statement3)     
        #    data3 = cursor.fetchall()
    
        #    try:
        #        url = "../the_project/media/" +  str(data3[0][0])
        #        with open(url, 'rb') as img:
        #            base64_string = base64.b64encode(img.read()).decode('utf-8')
        #            phot_list.append(base64_string)
        #    except:
        #        url = "../the_project/media/media/profile/default.jpg"
        #        with open(url, 'rb') as img:
        #            base64_string = base64.b64encode(img.read()).decode('utf-8')
        #            phot_list.append(base64_string)
            


        return JsonResponse({'user_data':data1,})


    
class team_list2(APIView):              #팀명 / 타임스탬프 / 팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def post(self,request):
        result_list = []
        cursor = connection.cursor()

        sql_statement1 = "select a.team_name, DATE_FORMAT(a.team_make_time,'%Y/%m/%d') from team_data a, team_user_data b where a.team_name = b.team_name and b.user_id = '" + request.data.get("id") + "';"
        #팀명과 타임스탬프
        result = cursor.execute(sql_statement1)      #코드 실행
        team_data = cursor.fetchall()                #실행 결과 입력
        for i in team_data:
            small_list = []
            team_user_sql = "select user_name from team_user_data a, user_data b where a.user_id = b.user_id and a.team_name = '" + i[0] + "';"
            #해당 팀에 속한 팀원을 보여줌
            result = cursor.execute(team_user_sql)      #코드 실행
            team_user_data = cursor.fetchall()          #실행 결과 입력

            small_list.append(i)
            small_list.append(team_user_data)
            result_list.append(small_list)

        return JsonResponse({'user_data':result_list})
        #팀에 대한 정보(팀명, 타임스탬프)와 팀원에 대한 정보를 함께 전달해주기 위해 for문을 사용함.



class team_list3(APIView):              #타임스탬프 / 팀소개 / 팀카테고리 / 팀원에 대한 정보를 보여주는 상세한 팀 리스트
    def post(self,request):
        data_list = []
        cursor = connection.cursor()
        sql_statement1 = "select introduction,DATE_FORMAT(team_make_time,'%Y/%m/%d'),team_category from team_data where team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement1)     
        team_data = cursor.fetchall()       
        data_list.append(team_data)

        sql_statement3 = "select a.user_name, a.user_email, a.user_comment, b.is_admin from user_data a, team_user_data b where a.user_id = b.user_id and team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()

        sql_statement = "select a.user_name, a.user_email, a.user_comment from user_data a, team_apply_log b where a.user_id = b.user_id and b.team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()

        return JsonResponse({'team_data':data_list,'user_datas':user_data,'apply_list':result_data})
        


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
        sql_statement3 = "select a.user_name, a.user_email, a.user_comment, b.is_admin from user_data a, team_user_data b where a.user_id = b.user_id and team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement3)     
        user_data = cursor.fetchall()

        return JsonResponse({'chk_message':'해당 팀원이 추방되었습니다!','datas':user_data})



class change_team_comment(APIView):     #팀 코맨트 변경
    def post(self,request):
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        team_data.introduction = request.data.get("teamcomment")
        team_data.save()
        return JsonResponse({'chk_message':'팀 코맨트가 수정되었습니다.'})





class team_apply(APIView):
    def post(self,request):
        chk = TeamApplyLog.objects.all()        #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user = request.data.get("id"),team_name = request.data.get("teamname")).exists():
            return JsonResponse({'message':'해당 팀은 이미 신청한 기록이 있습니다!'})

        result_data = TeamUserData.objects.filter(team_name = request.data.get("teamname")).annotate(Count('team_name')).aggregate(Count('team_name'))
        if result_data['team_name__count'] >= 8:
            return JsonResponse({'message':'해당 팀에 현재 남은 자리가 없습니다!'})

        apply_data = TeamApplyLog()
        apply_data.user = UserData.objects.get(user_id=request.data.get("id"))
        apply_data.team_name = TeamData.objects.get(team_name = request.data.get("teamname"))
        apply_data.save()
        return JsonResponse({'message':'팀 신청이 완료되었습니다.'})



class team_apply_list(APIView):
    def post(self,request):
        cursor = connection.cursor()
        sql_statement = "select a.user_name, a.user_email, a.user_comment from user_data a, team_apply_log b where a.user_id = b.user_id and b.team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        return JsonResponse({'apply_list': result_data})


class allow_apply(APIView):
    def post(self,request):
        user_data = UserData.objects.get(user_name=request.data.get("nickname"))
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        apply_data = TeamApplyLog.objects.get(user=user_data.user_id,team_name = team_data.team_name)
        apply_data.delete()

        user_datas = TeamUserData()
        user_datas.user = UserData.objects.get(user_id= user_data.user_id)
        user_datas.team_name = TeamData.objects.get(team_name = team_data.team_name)
        user_datas.is_admin = 0
        user_datas.save()

        cursor = connection.cursor()
        sql_statement = "select a.user_name, a.user_email, a.user_comment from user_data a, team_apply_log b where a.user_id = b.user_id and b.team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()

        sql_statement3 = "select a.user_name, a.user_email, a.user_comment, b.is_admin from user_data a, team_user_data b where a.user_id = b.user_id and team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement3)     
        user_datas = cursor.fetchall()



        return JsonResponse({'message':'새로운 팀원이 들어왔습니다.','apply_list':result_data,'user_datas':user_datas})



class reject_apply(APIView):
    def post(self,request):
        user_data = UserData.objects.get(user_name=request.data.get("nickname"))
        team_data = TeamData.objects.get(team_name = request.data.get("teamname"))
        apply_data = TeamApplyLog.objects.get(user=user_data.user_id,team_name = team_data.team_name)
        apply_data.delete()

        cursor = connection.cursor()
        sql_statement = "select a.user_name, a.user_email, a.user_comment from user_data a, team_apply_log b where a.user_id = b.user_id and b.team_name = '" + request.data.get("teamname") + "';"
        result = cursor.execute(sql_statement)     
        result_data = cursor.fetchall()
        
        return JsonResponse({'message':'신청을 거절했습니다!','apply_list': result_data})



class chat_log(APIView):
    def post(self,request):
        team_data = ChatData.objects.get(team_name = request.data.get("teamname"))


############################################ 게시글 관련



class post_list(APIView):       #게시판 들어갔을때 해당 게시판에 해당되는 글 리스트들 보여주는 코드
    def post(self,request):
        list = []               #게시글 리스트들

        cursor = connection.cursor()

        sql_statement1 = "select a.post_id, a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, date_format(a.post_time,'%Y-%m-%d %H:%i') 시간 from post_data a, user_data b where a.user_id = b.user_id and category = '" + request.data.get("category") + "'order by a.post_id desc;"
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
        sql_statement1 = "select a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, a.contents_data, a.team_name ,date_format(a.post_time,'%Y-%m-%d %H:%i') 시간 from post_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("post_id") + "';"
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

        return JsonResponse({'post_data':"작성이 완료되었습니다!"})



class recommend_this(APIView):               #추천 기능
    def post(self,request):
        ### 튜플 값이 변환이 안되서 폐기
        #cursor = connection.cursor()
        #sql_statement = "select num_of_recommend from post_data where post_id = '" + request.data.get("boardID") + "';"
        #result = cursor.execute(sql_statement)    
        #recommend_num = cursor.fetchall()
        #recommend = list(recommend_num)
        #the_recommend = recommend[0] + 1
        ### 튜플 값이 변환이 안되서 폐기

        recommend_num = request.data.get("recommendNum")
        post_data = PostData.objects.get(post_id=request.data.get("boardID"))
        post_data.num_of_recommend = recommend_num + 1
        post_data.save()

        cursor = connection.cursor()
        sql_statement = "select a.post_title, b.user_name, a.num_of_open, a.num_of_recommend, a.contents_data, a.team_name ,date_format(a.post_time,'%Y-%m-%d %H:%i') 시간 from post_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("boardID") + "';"
        #게시글 제목, 작성자 이름, 조회수, 추천수, 게시글 내용, 팀 이름(팀 구인 게시판의 경우), 작성날짜를 알려주는 쿼리문
        result1 = cursor.execute(sql_statement)     
        data = cursor.fetchall()

        return JsonResponse({'post_data':data})



class post_change(APIView):
    def post(self,request):

        post_data = PostData.objects.get(pk = request.data.get("post_id"))
        post_data.contents_data = request.data.get("text")
        post_data.post_title = request.data.get("title")
        if request.data.get("category") == 'Team':
            post_data.team_name = TeamData.objects.get(pk = request.data.get("teamname"))

        post_data.save()

        return JsonResponse({'chk_message':"게시글이 수정되었습니다."})



class post_delete(APIView):
    def post(self,request):
        post_data = PostData.objects.get(post_id = request.data.get("post_id"))
        post_data.delete()
        return JsonResponse({'chk_message':"게시글이 삭제되었습니다!"})



############################################ 댓글



class comment_write(APIView):
    def post(self,request):
        comment_data = CommentData()    #댓글 테이블 연결
        comment_data.comment_cont = request.data.get("comment")
        comment_data.user = UserData.objects.get(pk = request.data.get("id"))
        comment_data.post = PostData.objects.get(pk = request.data.get("boardID"))
        comment_data.comment_time = datetime.datetime.now()
        comment_data.save()


        cursor = connection.cursor()
        sql_statement = "select a.comment_id, a.comment_cont, b.user_name, date_format(a.comment_time,'%Y-%m-%d %H:%i') 작성시간, a.post_id, a.user_id from comment_data a, user_data b where a.user_id = b.user_id and post_id = '" + request.data.get("boardID") +"' order by a.comment_id desc;"
        result = cursor.execute(sql_statement)    
        data = cursor.fetchall()
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



############################################ 이미지 관련(테스트중)