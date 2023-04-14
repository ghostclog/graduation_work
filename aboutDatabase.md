============================================================
데이터베이스(About Database)
============================================================



데이터베이스 구조

-사용자 데이터(user_data)
  1. user_id(varchar 50): 웹/유니티 접속시 사용하는 사용자 아이디. 중복 불가
  2. user_pass(varchar 128): 웹/유니티 접속시 사용하는 사용자 비밀번호
  3. user_name(varchar 50): 웹/유니티 접속시 사용하는 사용자 닉네임. 중복 불가
  4. user_admin(char 1): withrium프로잭트의 관리자 및 매니저인지에 대한 여부를 파악하는 컬럼. 0인 경우 일반 사용자. 1인 경우 관리자
  5. login_state(char 1): 해당 유저가 유니티에 접속한 상태인지 알려주는 컬럼. 현재는 미사용.
  6. user_email(varchar 512): 사용자의 이메일.
  7. user_comment(varchar 1024): 사용자의 코맨트. 웹의 마이페이지, 팀원 목록, 사용자 프로필, 등에서 확인이 가능함.
  8. user_point(varchar 45): 사용자가 웹에서 커뮤니티 활동을 하며 획득한 포인트. 웹의 상정 페이지에서 사용이 가능함.

-팀 데이터(team_data)
  1. team_name(varchar 250): 팀명입니다. 중복 불가
  2. user_id(varchar 50): 해당 팀을 생성한 팀장입니다.
  3. introduction(varchar 1024): 팀 소개문구입니다.
  4. team_make_time(datetime): 팀이 생성된 시각입니다.
  5. team_category(varchar 128): 팀의 카테고리입니다.

-팀원 데이터(team_user_data)
  1. pr_key(int): 팀원 데이터 테이블의 키값으로 AutoIncrement입니다. 장고 구조의 문제로 인해 해당값을 추가하였습니다. 해당 컬럼을 실제로 사용하는 곳은 없습니다.
  2. team_name(varchar 250): 해당 유저가 속한 팀명입니다.
  3. user_id(varchar 50): 해당 팀에 속한 유저 아이디입니다.
  4. is_admin(char 1): 해당 유저가 해당 팀의 관리자 여부를 파악하는 컬럼입니다.

-팀 게시글 테이블(team_post)
  1. post_id(int): 게시글에 부여된 임의의 킷값입니다 AutoIncrement이며, 정렬할 때 사용
  2. post_title(varchar 50): 게시글 제목
  3. post_contents(text): 게시글의 내용
  4. post_time(datetime): 게시글이 포스팅된 시각. 정렬 할 때 사용.
  5. team_name(varchar 45): 해당 게시글이 어느 팀에 속한 게시글인지를 알려주는 컬럼.
  6. user_id(varchar 45): 게시글을 작성한 유저의 아이디.
  7. post_type(varchar 45): 게시글의 종류입니다. 일반 게시글(normal), 정보공유 게시글(share), 파일 첨부 게시글(file_save) 3종류로 나뉩니다.

-팀 신청 로그 테이블(team_apply_log)
  1. apply_id(int): 신청 로그 고유의 아이디값. AutoIncremen임.
  2. user_id(varchar 50): 팀 가입 신청을 요청한 사용자의 아이디
  3. tema_name(varchar 250): 사용자가 가입 신청을 한 팀명.

-쪽지함/알림함 테이블(message)
  1. message_id(int): 쪽지/알림 고유의 아이디값. AutoIncremen임.
  2. receiver_id(varchar 50): 쪽지/알림을 받는 사용자의 아이디.
  3. title(varchar 64): 쪽지/알림 제목
  4. contents(varchar 1024): 쪽지/알림의 내용
  5. category(varchar 45): 쪽지/알림의 종류
  6. receive_time(datetime): 쪽지/알림을 받은 시각
  7. about_chk(int): 쪽지/알림을 받은 사람이 해당 쪽지/알림을 확인했는지 여부

-게시글 테이블(post_data)
  1. post_id(int): 게시글 고유의 아이디. AutoIncremen임.
  2. category(varchar 45): 게시글 카테고리. 질문(Question), 정보 공유(Share), 팀 구인(Team) 세가지로 분류됨
  3. contents_data(varchar 50): 게시글의 내용.
  4. post_time(datetime): 게시글 작성 시간
  5. team_name(varchar 45): 해당 게시글이 팀 구인인 경우 어느 팀에 대한 구인인지에 대한 정보
  6. num_of_open(int): 게시글 조회수
  7. num_of_recommend(int): 게시글 추천수
  8. post_title(varchar 1024): 게시글 제목
  9. post_type(varchar 50): 게시글의 종류. 사용자가 검색 탭에서 자료를 찾아서 공유한 경우 share이며, 아닌 경우 null.

-댓글 테이블(comment_data)
  1. comment_id(int): 댓글 고유의 아이디. AutoIncremen임.
  2. comment_cont(varchar 1024): 댓글 내용.
  3. user_id(varchar 50): 댓글을 작성한 사용자 아이디.
  4. post_id(int): 댓글이 작성된 게시글 아이디.
  5. comment_time(datetime): 댓글이 작성된 시각.

-채팅 로그 테이블(chat_data)
  1. chat_id(int): 채팅 고유의 아이디. AutoIncremen임.
  2. user_chat(char 100): 채팅 내용.
  3. team_name(varchar 250): 해당 채팅이 발생한 팀.
  4. user_name(varchar 50): 채팅을 친 사용자의 ‘닉네임’
  5. chat_time(timestamp): 채팅을 친 시각.

-유저가 소유중인 아이템 테이블(user_item_log)
  1. log_id(int): 아이탬 소유 로그 고유의 아이디. AutoIncremen임.
  2. user_id(varchar 45): 해당 아이탬을 소유한 유저의 아이디
  3. item_id(varchar 45): 유저가 소유한 아이탬의 아이디
  4. item_category(varchar 45): 해당 아이탬이 치장탬(outfit)인지, 캐릭터(character)인지에 대한 여부

-프로필 사진 경로 저장 테이블(web_back_profile_photo)
  1. user_photo(varchar 100): 해당 사진의 경로 및 사진 파일명
  2. user_id(varchar 50): 해당 유저 아이디

-파일 첨부 팀 게시글의 파일 경로 테이블(web_back_team_file)
  1. the_post_id(int): 파일이 첨부된 게시글 아이디
  2. files(varchar 100): 첨부 파일의 경로 및 파일명



============================================================



데이터베이스 구조 설계 로그

-23년 1월 1일~ 2일: 첫 설계(당시 기록 없음.)

-1월 6일~9일:
  1. 기존의 팀원 구인 테이블 삭제 > 종합 게시글 테이블로 변경
  2. 댓글 테이블 구조 변경
  3. 팀 신청 테이블 삭제
  4. 팀 정보 테이블 컬럼 추가(소개 / 팀 생성 시각)
  5. 팀원 테이블 구조 수정(사유: 테이블명 및 컬럼명이 예약어로 되어있어, 사용하는데 불편함이 발생)
  6. 유저 테이블 컬럼 추가(이메일 / 유저 코맨트란)

-1월 10일: 
  1. 팀정보 테이블에 팀 카테고리 추가
  2. 장고 데이터베이스 구조 문제로 기존 팀원 테이블의 기본키였던 유저 아이디를 일반 외래키로 격하, int형 기본키 생성. 해당 기본키는 autoincreament임
  3. 코맨트 테이블의 기본키를 autoincreament로 변경

-1월 16일:
  1. 이미지 처리를 위한 테이블 추가
  2. 게시글 테이블 컬럼 추가(조회수, 추천수, 게시글 제목, 게시글 분류, 팀 이름)

-1월 27일: 기존 프로필 사진 테이블 컬럼명 수정. 사유는 예약어

-2월 14일:쪽지함 테이블 추가

-3월 17일:포인트 시스템 추가/상점 시스템 추가
