from django.shortcuts import render,HttpResponse
from django.http import JsonResponse,Http404
from django.contrib.auth import authenticate
from django.db import connection

from rest_framework.views import APIView

from .models import *


# Create your views here.
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
            change_name = UserData.objects.get(user_id = request.data.get("id") )
            change_name.user_pass = request.data.get("new_pw")
            change_name.save()
            return JsonResponse({'chk_message':'비밀번호가 변경되었습니다.'},status=200)
        else:
            return JsonResponse({'chk_message':'비밀번호가 틀렸습니다.'},status=200)



class email_change(APIView):      #이메일 변경(기존 닉네임 변경에서 코드만 살짝 수정함. 그래서 변수명은 닉네임 변경과 동일)
    def post(self,request):
        chk = UserData.objects.all()        #유저 테이블의 모든 객체를 가져옴
        if chk.filter(user_name = request.data.get("email")).exists():       #이메일 중복체크
            return JsonResponse({'chk_message':'이메일 중복입니다.'},status=200)
        change_name = UserData.objects.get(user_id = request.data.get("id") )
        change_name.user_name = request.data.get("email")
        change_name.save()
        return JsonResponse({'chk_message':'이메일이 변경되었습니다.'},status=200)


    
class into_mypage(APIView):      #비밀번호 변경
    def post(self,request):
        cursor = connection.cursor()
        #장고의 데이터베이스 연결 방식에서 파이썬 특유의 데이터베이스 연결 방식으로 코드를 바꿔봄.
        #사용해본 결과 데이터 입력 시에는 orm이 편한데. select문에 한해서는 쿼리문이 더편함
        sql_statement = "select user_email, user_comment from user_data where user_id ='" + request.data.get("id") + "';"       #입력한 아이디값에 맞는 이메일과 소개문을 반환
        result = cursor.execute(sql_statement)      #코드 실행
        data = cursor.fetchall()                   #실행 결과 입력
        connection.commit()                         #데이터베이스 변경 완료
        connection.close()                          #데이터베이스 접속 해제

        return JsonResponse({'user_data':data})    #data 자체는 튜플형식이나 json으로 보내지는 과정에서 알아서 배열로 바뀌는듯함. 프론트로에서 배열로 값이 왔다고함.