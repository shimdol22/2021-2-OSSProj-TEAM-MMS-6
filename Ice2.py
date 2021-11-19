import sys
import pygame
import random
import shelve
import time
from datetime import datetime
from pygame.constants import VIDEORESIZE
from math import ceil
# sx, sy => 피사체의 x위치 y 위치
# x, y => 비행기의 가로길이, 세로길이
# 1. 게임초기화
pygame.init()

# 2. 게임창 옵션 설정
# 2-1 고정된 화면 크기
# size = [700,800]
# screen = pygame.display.set_mode(size)

# 2-2 플레이어의 컴퓨터 환경에 맞춘 화면의 크기 
infoObject = pygame.display.Info()
# 896 * 1020
size = [infoObject.current_w,infoObject.current_h]
screen = pygame.display.set_mode(size,pygame.RESIZABLE)


class Move:
    # 좌방향 이동키
    left_go = False
    # 우방향 이동키
    right_go = False
    # 윗방향 이동키
    up_go = False
    # 아랫방향 이동키
    down_go = False
    # 미사일 발사 키
    space_go = False
    # 게임의 FPS
    FPS = 60
    # 객체의 변경된 위치변경의 Key
    position = False
    # 객체들이 화면 밖으로 나갔는지 판정에 필요한 boundary 값
    boundary = 0

class Color:
    # RGB 검정
    black = (0,0,0)
    # RGB 흰색
    white = (255,255,255)
    red = (255,0,0)
    purple = (100,40,225)
    yellow = (255,255,0)

class Size:
    # 피사체의 x,y사이즈
    a_xsize = size[0]//13
    a_ysize = size[1]//8
    # 미사일의 x,y사이즈
    m_xsize = size[0]//30
    m_ysize = size[1]//20
    # 미사일의 크기 조정(최대값, 최소값)
    min_size = ceil((sum(size)//35))
    max_size = ceil((sum(size)//20))
    block_max_size = size[0]//10
    # 2등분 3등분 값을 찾기위한 num
    half_split_num = 2
    third_split_num = 3
    three_five = 2/5

    m_rand_size = 10

    x_resize_rate = 1
    y_resize_rate = 1

    err_x = 400
    err_y = 500

    standard_size = 30

    rand_min_size = 1

    x = 0 
    y = 1

    restart_middle = 290


class Speed:
    # 미사일의 스피드
    m_speed = 0 # 초기화`
    m_initiate_speed_30 = 30
    m_initiate_speed_15 = 15
    # 미사일의 max 스피드
    m_max_speed = 6
    # 비행체 스피드
    s_speed =5
    # 미사일 빈도 조정 
    k=0
    create_rate_r = 0.995
    create_rate_c = 0.98
    # 미사일 스피드의 초기값 15 고정
    speed_initializing_15 = 15
    # 초기 스피드
    a_init_speed = 2
    m_init_speed = 2
    b_init_speed = 2

    speed_end_point = 0 


class Util:
    # 최고기록
    # 미사일을 발사할때 미사일 객체가 저장되는 리스트 공간
    m_list = []
    # 피사체 출현시 피사체 객체가 저장되는 리스트 공산
    a_list = []
    # 장애물 객체가 저장되는 리스트 
    block_list=[]
    # 피사체를 미사일로 맞추었을때 맞춘 피사체의 개수
    kill = 0 
    # 피사체를 죽이지못하고 화면밖으로 놓친 피사체의 개수
    loss = 0 
    # 현재 내가 획득한 점수
    score = 0
    # 최고점수 불러오기
    f = open('Icescore.txt', 'r')
    x = f.read()
    highscore = int(x)
    # Game Over
    GO = 0

    score_10 = 10
    score_100 = 100
    score_200 = 200
    score_300 = 300
    score_400 = 400

    m_loc_10 = 10
    a_loc_10 = 10
    start_loc = (0,0)

    kill_score_cal = 5
    loss_score_cal = 8

    missile_rate = 1

    obj_num = 1

    sleep_time = 1


class FontSize:
    size_start = 20
    lensize_start = 50
    size_kill_loss = sum(size) // 85
    size_gameover = sum(size) // 40
    size_restart = 15
    lensize_gameover = 65
    len_for_time = size[0] // 6
    len_for_time_ysize = 5
    loc_kill_loss = (10,5)


class Sound:
    m_sound = 0.1
    crash1_sound = 0.1
    crash2_sound = 0.1
    game_over_sound = 0.3
    background_sound = 0.1

class Resizing:
    a_xsize = 13
    a_ysize = 8
    m_xsize = 30
    m_ysize = 20

    min_size_rel = 35
    max_size_rel = 20
    min_size =  1
    max_size =  1

    block_max_size = 10

    size_kill_loss = 85
    size_gameover = 47
    len_for_time = 6



class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self,address):
        # png파일 일때
        # convert해줘야하는 문제가 있기때문에
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()    
        else: 
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()

    # 피사체의 그림 조정
    def change_size(self,sx,sy):
        self.img = pygame.transform.scale(self.img,(sx,sy)) # 그림의 크기를 조정한다.
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img,(self.x,self.y))






title = "My Game"
pygame.display.set_caption(title) # 창의 제목 표시줄 옵션
# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()
#파이게임 배경음악
pygame.mixer.init()
pygame.mixer.music.load("SourceCode/Sound/Rien.mp3")
# 미사일 효과음
missile1 = pygame.mixer.Sound("SourceCode/Sound/present1.mp3")
missile1.set_volume(Sound.m_sound)
missile2 = pygame.mixer.Sound("SourceCode/Sound/present2.mp3")
missile2.set_volume(Sound.m_sound)
missile3 = pygame.mixer.Sound("SourceCode/Sound/present4.mp3")
missile3.set_volume(Sound.m_sound)
# 피사체 파괴시 효과음
penguin = pygame.mixer.Sound("SourceCode/Sound/penguin.mp3")
penguin.set_volume(Sound.crash1_sound)
# 피사체와 비행체 충돌시 효과음
boom1 = pygame.mixer.Sound("SourceCode/Sound/puck.mp3")
boom1.set_volume(Sound.crash2_sound)
# 게임오버 효과음
game_over = pygame.mixer.Sound("SourceCode/Sound/gameover.wav")
game_over.set_volume(Sound.game_over_sound)


# 충돌이 일어났는지 확인하는 함수!
# return 값이 boolean 타입임
# 직사각형 형태로 충돌이 일어났음을 판단하는 함수
def crash(a,b):
    # 요 범위 안에 있을때 충돌이 일어남
    if (a.x-b.sx <=b.x) and (b.x<=a.x + a.sx):
        if(a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
            
    else:
        return False

# 기존 충돌판정에서 모든 모서리의 x,y값을 가지고 객체가 겹친다면 충돌이 일어나는 함수 생성
# 직사각현 모양에서 발생했던 부딛치지 않았지만 부딛혔다고 판정된 문제 해결
def crash2(a,b):
    a_mask = pygame.mask.from_surface(a.img)
    b_mask = pygame.mask.from_surface(b.img)

    offset = (int(b.x - a.x), int(b.y - a.y))
    collision = a_mask.overlap(b_mask, offset)
    
    if collision:
        return True
    else:
        return False


def cal_score(kill,loss):
    Util.score = (Util.kill * Util.kill_score_cal - Util.loss * Util.loss_score_cal)


def change_size_rate(size):
    
    Size.a_xsize = size[Size.x] // Resizing.a_xsize
    Size.a_ysize = size[Size.y] // Resizing.a_ysize
    Size.m_xsize = size[Size.x] // Resizing.m_xsize
    Size.m_ysize = size[Size.y] // Resizing.m_ysize
    Size.min_size = ceil((sum(size) // Resizing.min_size_rel ) * Resizing.min_size)
    Size.max_size = ceil((sum(size) // Resizing.max_size_rel ) * Resizing.max_size)
    Size.block_max_size = size[Size.x] // Resizing.block_max_size
    FontSize.size_kill_loss = sum(size) // Resizing.size_kill_loss
    FontSize.size_gameover = sum(size) // Resizing.size_gameover
    FontSize.len_for_time = size[Size.x] // Resizing.len_for_time
    
    
    # # 오른쪽 끝 선에서 크기를 줄일 시 객체가 화면 밖으로 못나가게 제한 함
    # if ss.x + ss.sx > size[0]:
    #     ss.x = size[0]- ss.sx
    # # 바닥 선에서 크기를 줄일 시 객체가 화면 밖으로 못나가게 제한 함
    # if ss.y + ss.sy >size[1]:
    #     ss.y = size[1] - ss.sy
    # 비행체 객체의 사이즈 변경
    try:
        ss.put_img("SourceCode/Image/santa.png")
        ss.change_size(Size.a_xsize, Size.a_ysize)
        ss.x*=Size.x_resize_rate
        ss.y*=Size.y_resize_rate
    except :
        pass
    try:
        # 지금 현재 미사일을 발생시키지 않는 상태 일 수도 있기 때문에 try, except구문 사용
        for i in Util.m_list:
            i.change_size(int(i.sx*Size.x_resize_rate),int(i.sy*Size.y_resize_rate))
    except :
        pass
    # 선인장 장애물의 resizing
    # 선인장이 나타나지 않았을때 resizing 했을 수도 있으므로 try except로 error 잡아줌
    try:
        for i in Util.block_list:
            i.change_size(int(i.sx*Size.x_resize_rate),int(i.sy*Size.y_resize_rate))
            i.x*=Size.x_resize_rate
            i.y*=Size.y_resize_rate
            
    except :
        pass
    try:
        for i in Util.a_list:
            i.change_size(ceil(i.sx*Size.x_resize_rate),ceil(i.sy*Size.y_resize_rate))
            if a.sx > Size.err_x or a.sy > Size.err_y:
                i.change_size(Size.standard_size,Size.standard_size)
                # print(a.sx,a.sy)
            i.x*=Size.x_resize_rate
            i.y*=Size.y_resize_rate
    except :
        pass
    # FPS도 리사이징이 됨에따라 변화시켜주고 속도제어
    Move.FPS = int(Move.FPS*(Size.x_resize_rate+Size.y_resize_rate)/Size.half_split_num)
    pygame.display.flip()


# 4-0 게임 시작 대기 화면(작은 event)
# SB=0
# while SB==0:
#     clock.tick(Move.FPS)
#     for event in pygame.event.get(): # 이벤트가 있다면 
#         if event.type == pygame.KEYDOWN: # 그 이벤트가 어떤 버튼을 누르는 것이라면
#             if event.key == pygame.K_SPACE: # 그 버튼이 스페이스 버튼이라면?
#                 SB=1
#         elif event.type == pygame.VIDEORESIZE:
#             width, height = event.w, event.h
#             size =[width,height]
#             window = pygame.display.set_mode(size, pygame.RESIZABLE)
#     screen.fill(Color.black)

#     font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf",FontSize.size_start)
#     text_kill = font.render("PRESS \"SPACE\" KEY TO START THE GAME",True,Color.white) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
#     screen.blit(text_kill,(size[0]//Size.half_split_num-(size[0]//Size.half_split_num)//Size.half_split_num,round((size[1]/Size.half_split_num)-FontSize.lensize_start))) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 

#     pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨

# 객체 생성
ss = obj()
# 우리들이 움직여야할 물체
ss.put_img("SourceCode/Image/santa.png")
# 그림(비행체)의 크기를 조정
ss.change_size(Size.a_xsize,Size.a_ysize)
# 비행체의 위치를 하단의 중앙으로 바꾸기위해!
# x값의 절반에서 피사체의 길이의 절반만큼 왼쪽으로 이동해야 정확히 가운데임
ss.x = round(size[0]/Size.half_split_num - ss.sx/Size.half_split_num)
# 맨 밑에서 피사체의 y길이만큼 위로 올라와야함
ss.y = size[1] - ss.sy
# 비행체가 움직이는 속도를 결정함
ss.move = Speed.s_speed

# 게임의 배경화면 설정
background_image_desert = pygame.image.load("SourceCode/Image/Antartic.png")
background_image_desert = pygame.transform.scale(background_image_desert,size) # 그림의 크기를 조정한다.



# 4. 메인 이벤트
#사막맵 배경음악 실행
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(Sound.background_sound)
# 코드를 첫 실행한 시간 저장
start_time = datetime.now()
SB = False
while not SB:
    # 4-1. FPS 설정 
    # FPS를 60으로 설정함
    clock.tick(Move.FPS)

    # 4-2. 각종 입력 감지 
    for event in pygame.event.get():  # 어떤 동작을 했을때 그 동작을 받아옴
        if event.type == pygame.QUIT: # x버튼을 눌렀을때!
            SB = True # SB 가 1이되면 while문을 빠져나오게 된다!
        if event.type == pygame.KEYDOWN: # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
            # 키를 누르고있는 상태 : True
            # 키를 떼고있는 상태 : False
            if event.key == pygame.K_LEFT:  # 만약 누른 키가 왼쪽 방향키 라면?
                Move.left_go = True
            if event.key == pygame.K_RIGHT:  # 만약 누른 키가 오른쪽 방향키 라면?
                Move.right_go = True
            if event.key == pygame.K_SPACE:  # 만약 누른키가 space키 라면?
                Move.space_go = True
                # 속도를 1/6으로 낮췄는데 누를때마다도 한번씩 발사하고싶어서 누르면 k=0으로 초기화시킴 -> while문 조건 통과하기위해
                # k=0
            if event.key == pygame.K_UP :
                Move.up_go = True
            if event.key == pygame.K_DOWN:
                Move.down_go = True
            
        elif event.type == pygame.KEYUP: # 키를 누르는것을 뗐을때!
            if event.key == pygame.K_LEFT: # 키를 뗐다면 그 키가 왼쪽 방향키 인가?
                Move.left_go = False
            elif event.key == pygame.K_RIGHT: # 키를 뗐다면 그 키가 오른쪽 방향키 인가?
                Move.right_go = False
            elif event.key == pygame.K_SPACE: # 키를 뗐다면 그 키가 스페이스 키인가?
                Move.space_go = False
            elif event.key == pygame.K_UP:
                Move.up_go = False
            elif event.key == pygame.K_DOWN:
                Move.down_go = False
        
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            Size.x_resize_rate = width / size[Size.x]
            Size.y_resize_rate = height / size[Size.y]
            size =[width,height]
            window = pygame.display.set_mode(size, pygame.RESIZABLE)
            Move.position = True
            

    # 마우스로 인해 화면이 작아지면 다른 객체들의 사이즈도 전부 변경
    if Move.position is True:
        change_size_rate(size)
    
    
    
        # 4-3. 입력과 시간에 따른 변화 
    now_time = datetime.now()
        # 코드실행 시점에서 현재시간과릐 차이를 초로 바꿈
    delta_time = (now_time - start_time).total_seconds()


    # 버튼을 꾹 길게 눌렀을때 움직이게 하기
    # 왼쪽 방향키를 눌렀을 때
    if Move.left_go == True:
        ss.x -= ss.move
        # 물체가 왼쪽 끝 경계값으로 이동하면 더이상 나가지 않게끔 만듬!
        # 배경이 뭐냐에 따라 달라질 듯 !
        if ss.x < Move.boundary:
            # 더 이상 나가지 못하도록 0 으로 막아줌
            ss.x = Move.boundary 
    # 오른쪽 방향키를 눌렀을 때
    elif Move.right_go == True:
        ss.x += ss.move
        # 오른쪽 끝에서 비행선의 가로크기만큼 빼줘야한다
        if ss.x >= size[Size.x] - ss.sx:
            # 더 이상 오른쪽 바깥으로 못나가게 오른쪽 끝값으로 초기화
            ss.x = size[Size.x] - ss.sx
    # 윗 방향키를 눌렀을때
    # 윗 방향키를 elif에서 if로 시작
    # 좌우와 상하가 독립된 상태로 구분됨
    if Move.up_go == True:
        ss.y -= ss.move
        # 게임화면 위쪽 화면으로 나가는 경우
        if ss.y < Move.boundary:
            # 더이상 나가지 못하게 위치값 고정
            ss.y = Move.boundary
    # 아래 방향키를 눌렀을때
    elif Move.down_go == True:
        ss.y += ss.move
        # 게임화면 위쪽 화면으로 나가는 경우
        if ss.y >= size[Size.y] - ss.sy:
            # 더이상 나가지 못하게 위치값 고정
            ss.y = size[Size.y] - ss.sy


    # 미사일의 속도 조정
    if Speed.m_initiate_speed_30-(Util.score // Util.score_10)>=Speed.m_max_speed:
        m_speed = Speed.m_initiate_speed_30 - (Util.score // Util.score_10)
    else:
        m_speed = Speed.m_max_speed



    # 점수와 관련해서 미사일의 속도를 바꾸면 좋을듯 !
    # k%6 이면 미사일의 발생 확률을 1/6으로  낮춤!
    if (Move.space_go == True) and Speed.k % m_speed == Speed.speed_end_point:
        # 미사일 객체 생성
        mm = obj()
        # 미사일의 사진
        mm.put_img('SourceCode/Image/ice_missile.png')
        # 미사일의 크기 조정
        # m_xsize = 5, m_ysize = 15
        mm.change_size(Size.m_xsize,Size.m_ysize)
        # 미사일 생성시 효과음
        missile1.play()
        # 미사일의 x값 (위치)
        if Util.score < Util.score_200:
            mm.x = round(ss.x + ss.sx / Size.half_split_num - mm.sx / Size.half_split_num)
            # 미사일의 위치 = 비행기의 위치 - 미사일의 y크기 
            mm.y = ss.y - mm.sy - Util.m_loc_10
        elif Util.score >= Util.score_200 and Util.score < Util.score_400:
            mm.x = round(ss.x + ss.sx / Size.third_split_num - mm.sx / Size.half_split_num)
            # 미사일의 위치 = 비행기의 위치 - 미사일의 y크기 
            mm.y = ss.y - mm.sy - Util.m_loc_10
        elif Util.score >= Util.score_400:
            mm.x = round(ss.x + ss.sx / Size.half_split_num - mm.sx / Size.half_split_num)
            mm.y = ss.y - mm.sy - Util.m_loc_10
        
        
        # 미사일의 움직이는 속도를 결정함
        mm.move = Speed.m_initiate_speed_15
        # 미사일의 객체를 리스트에 저장한다.
        Util.m_list.append(mm)

    # 점수가 200점 이상이라면 미사일이 한개 더 늘어남
    # 점수가 400점 이상이라면 미사일의 발사 형태가 바뀜
    if (Move.space_go == True) and (Speed.k%m_speed == Speed.speed_end_point) and Util.score >= Util.score_200:
        # 두번째 미사일 객체 생성
        missile1.stop()
        missile2.play()
        mm2 = obj()
        mm2.put_img('SourceCode/Image/ice_missile.png')
        mm2.change_size(Size.m_xsize, Size.m_ysize)
        mm2.x = round(ss.x +(ss.sx * Size.half_split_num) / Size.third_split_num - mm.sx / Size.half_split_num)
        mm2.y = ss.y - mm2.sy - Util.m_loc_10
        mm2.move = Speed.m_initiate_speed_15
        Util.m_list.append(mm2)


    # 미사일의 발생 빈도 조절
    Speed.k += Util.missile_rate

    # 피사체의 리스트를 초기화함
    # delete list
    d_list = []
    for i in range(len(Util.m_list)):
        # i 번째 미사일
        m = Util.m_list[i]
        # 미사일 속도만큼 미사일이 y축방향으로 빠져나간다.
        m.y -= m.move
        if Util.score > Util.score_400:
            missile2.stop()
            missile3.play()
            # 점수가 400점 이상이면 미사일이 꼬여서 나가는것 처럼 보이게 함
            m.x+= random.uniform(-Util.m_loc_10,Util.m_loc_10)
        # 미사일의 사이즈만큼 나갔을때 지워준다.
        if m.y < -m.sx:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del Util.m_list[d]
    
    # score 400점마다 비행체의 속도 1씩 증가
    Speed.s_speed = Speed.s_speed + Util.score // Util.score_400


    # score 가 10점 증가함에따라 피사체 발생 개수 0.01확률 증가 
    if random.random() > Speed.create_rate_c - (Util.score//Util.score_100)/Util.score_100:
        # 피사체 객체 생성
        aa = obj()
        aa.put_img("SourceCode/Image/penguin2-removebg-preview.png")
        # 피사체의 그림 크기 조정
        random_size = random.randint(Size.min_size,Size.max_size)
        # print("Size.min_size : {} Size.max_size : {} ss.x : {} ss.y : {} ss.sx : {} ss.sy : {} size : {} aa.sx : {} aa.sy : {}".format(Size.min_size, Size.max_size,ss.x,ss.y,ss.sx,ss.sy,size,aa.sx,aa.sy))
        # 정사각형 모양의 피사체
        # 이미 사이즈가 한번 바뀌었으므로 다시 바뀔 필요가 없음 또 바꾸면 오류 발생
        if Move.position is not True:
            aa.change_size(random_size,random_size)
        aa.change_size(random_size,random_size)
        # 0부터 오른쪽 끝까지의 랜덤변수인데 비행기크기보다 작으므로 미사일을 안맞는 외계인도 고려해야함(비행선크기/2 를 뺴줘야함)
        aa.x = random.randrange(Size.rand_min_size, size[Size.x] - aa.sx - round(ss.sx/Size.half_split_num))
        aa.y = Util.a_loc_10
        aa.move = Speed.a_init_speed + (Util.score//Util.score_300)
        Util.a_list.append(aa)
    
    # 장애물 등장
    if random.random() > Speed.create_rate_r:
        # 장애물 객체 생성
        block = obj()
        block.put_img('SourceCode/Image/ship.png')
        random_size = random.randint(Size.min_size,Size.block_max_size)
        block.change_size(random_size, random_size)
        # block.change_size(Size.block_size, Size.block_size)
        block.x = Util.a_loc_10
        block.y = random.randint(Size.rand_min_size, size[Size.x] - block.sx - round(ss.sx/Size.half_split_num))
        block.move = Speed.b_init_speed + (Util.score//Util.score_100)
        Util.block_list.append(block)

    d2_list=[]
    for i in range(len(Util.block_list)):
        b = Util.block_list[i]
        b.x += b.move
        if b.x >= size[Size.x]:
            d2_list.append(i)

    d2_list.reverse()
    for d2 in d2_list:
        del Util.block_list[d2]


    # 살생부 리스트 초기화
    d_list = []
    for i in range(len(Util.a_list)):
        a = Util.a_list[i]
        a.y += a.move
        # 외계인이 화면 밖으로 나갔다면 지워준다.
        if a.y >= size[Size.y]:
            d_list.append(i)

    # 메모리 효율을 위해 삭제
    # 앞에서 부터 지워지면 리스트가 앞당겨져서 오류가 일어나기때문에 reverse해주고 지워준다.
    d_list.reverse()
    for d in d_list:
        del Util.a_list[d]
        # 외계인이 화면 밖으로 나간 횟수
        Util.loss += Util.obj_num

    dm_list = []
    da_list = []

    for i in range(len(Util.m_list)):
        for j in range(len(Util.a_list)):
            m = Util.m_list[i]
            a = Util.a_list[j]
            if crash(m,a) is True:
                dm_list.append(i)
                da_list.append(j)
    
    # 미사일2개와 외계인 1개가 같이 만나는 경우가 있을 수도 있으니까 배제하기위해 중복제거를 해준다.
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))
    # reverse 하지않고 지우면 앞에서 부터 지워지고 앞에서부터지워지면 index의 변화가 일어나서 reverse를 해야함
    dm_list.reverse()
    da_list.reverse()


    # del로 미사일과 외계인 삭제하기
    try:
        for dm in dm_list:
            del Util.m_list[dm]
    except :
        pass
    try:
        for da in da_list:
            del Util.a_list[da]
            # 피사체 사망시 효과음
            penguin.play()
            # 피사체를 파괴한 횟수
            Util.kill += Util.obj_num
    except :
        pass

    

    for i in range(len(Util.a_list)):
        a = Util.a_list[i]
        # 만약 외계인이 ss 와 부딛치면 게임 종료
        if crash2(a,ss) is True:
            # 부딛칠 때 효과음
            boom1.play()
            # 1초뒤에 꺼지도록 함
            time.sleep(Util.sleep_time)
            # while 문이 종료되도록 하는 key
            SB = True
            # Go 가 0 인상태로 while문을 빠져나왔다면 x버튼으로 빠져나온것
            Util.GO = True


    for i in range(len(Util.block_list)):
        b = Util.block_list[i]
        # 만약 장애물과 ss가 부딛치면 게임 종료시킴
        if crash2(b,ss) is True:
            # 부딛칠 때 효과음
            boom1.play()
            time.sleep(Util.sleep_time)
            # while문 종료 키 
            SB = True
            Util.GO = True


    # score 가 0 점이 되면 프로그램 종료
    if Util.score < 0:
        SB = True
        Util.GO = True
    


    # 4-4. 그리기 
    #  마우스에의해 창크기가 바뀜에 따라 배경화면 크기가 바뀜
    background_image_desert = pygame.image.load("SourceCode/Image/Antartic.png")
    background_image_desert = pygame.transform.scale(background_image_desert, size)
    screen.blit(background_image_desert, Util.start_loc)
    

    # 비행체 보여주기
    ss.show()
    # 미사일 보여주기
    for m in Util.m_list:
        m.show()
    # 피사체 보여주기
    for a in Util.a_list:
        # print(a.sx,a.sy)
        if (a.sx > Size.err_x) or (a.sy > Size.err_y):
            a.put_img("SourceCode/Image/penguin2-removebg-preview.png")
            a.change_size(Size.standard_size,Size.standard_size)
        a.show()
    # 선인장 장애물 보여주기
    for d in Util.block_list:
        d.show()
    # 점수 산정
    # Util.score = (Util.kill*5 - Util.loss*8)
    # 점수산정을 메소드화 하였음
    cal_score(Util.kill, Util.loss)
    
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf", FontSize.size_kill_loss)

    text_kill = font.render("Killed : {} Loss : {}  Score : {} HighScore : {}".format(Util.kill, Util.loss, Util.score, Util.highscore), True, Color.yellow) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔

    screen.blit(text_kill,FontSize.loc_kill_loss) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
    # 현재 흘러간 시간
    text_time = font.render("Time : {:.2f}".format(delta_time), True, Color.purple)
    screen.blit(text_time,(size[0]-FontSize.len_for_time, FontSize.len_for_time_ysize))
    
    # 4-5. 업데이트
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨
    Move.position = False


def restart():
    # 2. 게임창 옵션 설정
    # 2-1 고정된 화면 크기
    # size = [700,800]
    # screen = pygame.display.set_mode(size)
    #pygame.init()
    class Move:
    # 좌방향 이동키
        left_go = False
        # 우방향 이동키
        right_go = False
        # 윗방향 이동키
        up_go = False
        # 아랫방향 이동키
        down_go = False
        # 미사일 발사 키
        space_go = False
        # 게임의 FPS
        FPS = 60
        # 객체의 변경된 위치변경의 Key
        position = False
        # 객체들이 화면 밖으로 나갔는지 판정에 필요한 boundary 값
        boundary = 0

    title = "My Game"
    pygame.display.set_caption(title) # 창의 제목 표시줄 옵션
    # 3. 게임 내 필요한 설정
    clock = pygame.time.Clock()
    #파이게임 배경음악
    pygame.mixer.init()
    pygame.mixer.music.load("SourceCode/Sound/Rien.mp3")
    # 미사일 효과음
    missile1 = pygame.mixer.Sound("SourceCode/Sound/present1.mp3")
    missile1.set_volume(Sound.m_sound)
    missile2 = pygame.mixer.Sound("SourceCode/Sound/present2.mp3")
    missile2.set_volume(Sound.m_sound)
    missile3 = pygame.mixer.Sound("SourceCode/Sound/present4.mp3")
    missile3.set_volume(Sound.m_sound)
    # 피사체 파괴시 효과음
    penguin = pygame.mixer.Sound("SourceCode/Sound/penguin.mp3")
    penguin.set_volume(Sound.crash1_sound)
    # 피사체와 비행체 충돌시 효과음
    boom1 = pygame.mixer.Sound("SourceCode/Sound/puck.mp3")
    boom1.set_volume(Sound.crash2_sound)
    # 게임오버 효과음
    game_over = pygame.mixer.Sound("SourceCode/Sound/gameover.wav")
    game_over.set_volume(Sound.game_over_sound)
    # 2-2 플레이어의 컴퓨터 환경에 맞춘 화면의 크기 
    infoObject = pygame.display.Info()
    # 896 * 1020
    size = [infoObject.current_w,infoObject.current_h]
    screen = pygame.display.set_mode(size,pygame.RESIZABLE)
    # 객체 생성
    ss = obj()
    # 우리들이 움직여야할 물체
    ss.put_img("SourceCode/Image/santa.png")
    # 그림(비행체)의 크기를 조정
    ss.change_size(Size.a_xsize,Size.a_ysize)
    # 비행체의 위치를 하단의 중앙으로 바꾸기위해!
    # x값의 절반에서 피사체의 길이의 절반만큼 왼쪽으로 이동해야 정확히 가운데임
    ss.x = round(size[0]/Size.half_split_num - ss.sx/Size.half_split_num)
    # 맨 밑에서 피사체의 y길이만큼 위로 올라와야함
    ss.y = size[1] - ss.sy
    # 비행체가 움직이는 속도를 결정함
    ss.move = Speed.s_speed

    # 게임의 배경화면 설정
    background_image_desert = pygame.image.load("SourceCode/Image/Antartic.png")
    background_image_desert = pygame.transform.scale(background_image_desert,size) # 그림의 크기를 조정한다.

    # 4. 메인 이벤트
    #사막맵 배경음악 실행
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(Sound.background_sound)
    start_time = datetime.now()
    SB = False
    while not SB:
        # 4-1. FPS 설정 
        # FPS를 60으로 설정함
        clock.tick(Move.FPS)
        # 4-2. 각종 입력 감지 
        for event in pygame.event.get():  # 어떤 동작을 했을때 그 동작을 받아옴
            if event.type == pygame.QUIT: # x버튼을 눌렀을때!
                SB = True # SB 가 1이되면 while문을 빠져나오게 된다!
            if event.type == pygame.KEYDOWN: # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
                # 키를 누르고있는 상태 : True
                # 키를 떼고있는 상태 : False
                if event.key == pygame.K_LEFT:  # 만약 누른 키가 왼쪽 방향키 라면?
                    Move.left_go = True
                if event.key == pygame.K_RIGHT:  # 만약 누른 키가 오른쪽 방향키 라면?
                    Move.right_go = True
                if event.key == pygame.K_SPACE:  # 만약 누른키가 space키 라면?
                    Move.space_go = True
                    # 속도를 1/6으로 낮췄는데 누를때마다도 한번씩 발사하고싶어서 누르면 k=0으로 초기화시킴 -> while문 조건 통과하기위해
                    # k=0
                if event.key == pygame.K_UP :
                    Move.up_go = True
                if event.key == pygame.K_DOWN:
                    Move.down_go = True
                
            elif event.type == pygame.KEYUP: # 키를 누르는것을 뗐을때!
                if event.key == pygame.K_LEFT: # 키를 뗐다면 그 키가 왼쪽 방향키 인가?
                    Move.left_go = False
                elif event.key == pygame.K_RIGHT: # 키를 뗐다면 그 키가 오른쪽 방향키 인가?
                    Move.right_go = False
                elif event.key == pygame.K_SPACE: # 키를 뗐다면 그 키가 스페이스 키인가?
                    Move.space_go = False
                elif event.key == pygame.K_UP:
                    Move.up_go = False
                elif event.key == pygame.K_DOWN:
                    Move.down_go = False
            
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                Size.x_resize_rate = width / size[Size.x]
                Size.y_resize_rate = height / size[Size.y]
                size =[width,height]
                window = pygame.display.set_mode(size, pygame.RESIZABLE)
                Move.position = True
                

        # 마우스로 인해 화면이 작아지면 다른 객체들의 사이즈도 전부 변경
        if Move.position is True:
            change_size_rate(size)
        
        
        
            # 4-3. 입력과 시간에 따른 변화 
        now_time = datetime.now()
            # 코드실행 시점에서 현재시간과릐 차이를 초로 바꿈
        delta_time = (now_time - start_time).total_seconds()


        # 버튼을 꾹 길게 눌렀을때 움직이게 하기
        # 왼쪽 방향키를 눌렀을 때
        if Move.left_go == True:
            ss.x -= ss.move
            # 물체가 왼쪽 끝 경계값으로 이동하면 더이상 나가지 않게끔 만듬!
            # 배경이 뭐냐에 따라 달라질 듯 !
            if ss.x < Move.boundary:
                # 더 이상 나가지 못하도록 0 으로 막아줌
                ss.x = Move.boundary 
        # 오른쪽 방향키를 눌렀을 때
        elif Move.right_go == True:
            ss.x += ss.move
            # 오른쪽 끝에서 비행선의 가로크기만큼 빼줘야한다
            if ss.x >= size[Size.x] - ss.sx:
                # 더 이상 오른쪽 바깥으로 못나가게 오른쪽 끝값으로 초기화
                ss.x = size[Size.x] - ss.sx
        # 윗 방향키를 눌렀을때
        # 윗 방향키를 elif에서 if로 시작
        # 좌우와 상하가 독립된 상태로 구분됨
        if Move.up_go == True:
            ss.y -= ss.move
            # 게임화면 위쪽 화면으로 나가는 경우
            if ss.y < Move.boundary:
                # 더이상 나가지 못하게 위치값 고정
                ss.y = Move.boundary
        # 아래 방향키를 눌렀을때
        elif Move.down_go == True:
            ss.y += ss.move
            # 게임화면 위쪽 화면으로 나가는 경우
            if ss.y >= size[Size.y] - ss.sy:
                # 더이상 나가지 못하게 위치값 고정
                ss.y = size[Size.y] - ss.sy


        # 미사일의 속도 조정
        if Speed.m_initiate_speed_30-(Util.score // Util.score_10)>=Speed.m_max_speed:
            m_speed = Speed.m_initiate_speed_30 - (Util.score // Util.score_10)
        else:
            m_speed = Speed.m_max_speed

        # 점수와 관련해서 미사일의 속도를 바꾸면 좋을듯 !
        # k%6 이면 미사일의 발생 확률을 1/6으로  낮춤!
        if (Move.space_go == True) and Speed.k % m_speed == Speed.speed_end_point:
            # 미사일 객체 생성
            mm = obj()
            # 미사일의 사진
            mm.put_img('SourceCode/Image/ice_missile.png')
            # 미사일의 크기 조정
            # m_xsize = 5, m_ysize = 15
            mm.change_size(Size.m_xsize,Size.m_ysize)
            # 미사일 생성시 효과음
            missile1.play()
            # 미사일의 x값 (위치)
            if Util.score < Util.score_200:
                mm.x = round(ss.x + ss.sx / Size.half_split_num - mm.sx / Size.half_split_num)
                # 미사일의 위치 = 비행기의 위치 - 미사일의 y크기 
                mm.y = ss.y - mm.sy - Util.m_loc_10
            elif Util.score >= Util.score_200 and Util.score < Util.score_400:
                mm.x = round(ss.x + ss.sx / Size.third_split_num - mm.sx / Size.half_split_num)
                # 미사일의 위치 = 비행기의 위치 - 미사일의 y크기 
                mm.y = ss.y - mm.sy - Util.m_loc_10
            elif Util.score >= Util.score_400:
                mm.x = round(ss.x + ss.sx / Size.half_split_num - mm.sx / Size.half_split_num)
                mm.y = ss.y - mm.sy - Util.m_loc_10
            
            
            # 미사일의 움직이는 속도를 결정함
            mm.move = Speed.m_initiate_speed_15
            # 미사일의 객체를 리스트에 저장한다.
            Util.m_list.append(mm)

        # 점수가 200점 이상이라면 미사일이 한개 더 늘어남
        # 점수가 400점 이상이라면 미사일의 발사 형태가 바뀜
        if (Move.space_go == True) and (Speed.k%m_speed == Speed.speed_end_point) and Util.score >= Util.score_200:
            # 두번째 미사일 객체 생성
            missile1.stop()
            missile2.play()
            mm2 = obj()
            mm2.put_img('SourceCode/Image/ice_missile.png')
            mm2.change_size(Size.m_xsize, Size.m_ysize)
            mm2.x = round(ss.x +(ss.sx * Size.half_split_num) / Size.third_split_num - mm.sx / Size.half_split_num)
            mm2.y = ss.y - mm2.sy - Util.m_loc_10
            mm2.move = Speed.m_initiate_speed_15
            Util.m_list.append(mm2)


        # 미사일의 발생 빈도 조절
        Speed.k += Util.missile_rate

        # 피사체의 리스트를 초기화함
        # delete list
        d_list = []
        for i in range(len(Util.m_list)):
            # i 번째 미사일
            m = Util.m_list[i]
            # 미사일 속도만큼 미사일이 y축방향으로 빠져나간다.
            m.y -= m.move
            if Util.score > Util.score_400:
                missile2.stop()
                missile3.play()
                # 점수가 400점 이상이면 미사일이 꼬여서 나가는것 처럼 보이게 함
                m.x+= random.uniform(-Util.m_loc_10,Util.m_loc_10)
            # 미사일의 사이즈만큼 나갔을때 지워준다.
            if m.y < -m.sx:
                d_list.append(i)
        d_list.reverse()
        for d in d_list:
            del Util.m_list[d]
        
        # score 400점마다 비행체의 속도 1씩 증가
        Speed.s_speed = Speed.s_speed + Util.score // Util.score_400


        # score 가 10점 증가함에따라 피사체 발생 개수 0.01확률 증가 
        if random.random() > Speed.create_rate_c - (Util.score//Util.score_100)/Util.score_100:
            # 피사체 객체 생성
            aa = obj()
            aa.put_img("SourceCode/Image/penguin2-removebg-preview.png")
            # 피사체의 그림 크기 조정
            random_size = random.randint(Size.min_size,Size.max_size)
            # print("Size.min_size : {} Size.max_size : {} ss.x : {} ss.y : {} ss.sx : {} ss.sy : {} size : {} aa.sx : {} aa.sy : {}".format(Size.min_size, Size.max_size,ss.x,ss.y,ss.sx,ss.sy,size,aa.sx,aa.sy))
            # 정사각형 모양의 피사체
            # 이미 사이즈가 한번 바뀌었으므로 다시 바뀔 필요가 없음 또 바꾸면 오류 발생
            if Move.position is not True:
                aa.change_size(random_size,random_size)
            aa.change_size(random_size,random_size)
            # 0부터 오른쪽 끝까지의 랜덤변수인데 비행기크기보다 작으므로 미사일을 안맞는 외계인도 고려해야함(비행선크기/2 를 뺴줘야함)
            aa.x = random.randrange(Size.rand_min_size, size[Size.x] - aa.sx - round(ss.sx/Size.half_split_num))
            aa.y = Util.a_loc_10
            aa.move = Speed.a_init_speed + (Util.score//Util.score_300)
            Util.a_list.append(aa)
        
        # 장애물 등장
        if random.random() > Speed.create_rate_r:
            # 장애물 객체 생성
            block = obj()
            block.put_img('SourceCode/Image/ship.png')
            random_size = random.randint(Size.min_size,Size.block_max_size)
            block.change_size(random_size, random_size)
            # block.change_size(Size.block_size, Size.block_size)
            block.x = Util.a_loc_10
            block.y = random.randint(Size.rand_min_size, size[Size.x] - block.sx - round(ss.sx/Size.half_split_num))
            block.move = Speed.b_init_speed + (Util.score//Util.score_100)
            Util.block_list.append(block)

        d2_list=[]
        for i in range(len(Util.block_list)):
            b = Util.block_list[i]
            b.x += b.move
            if b.x >= size[Size.x]:
                d2_list.append(i)

        d2_list.reverse()
        for d2 in d2_list:
            del Util.block_list[d2]


        # 살생부 리스트 초기화
        d_list = []
        for i in range(len(Util.a_list)):
            a = Util.a_list[i]
            a.y += a.move
            # 외계인이 화면 밖으로 나갔다면 지워준다.
            if a.y >= size[Size.y]:
                d_list.append(i)

        # 메모리 효율을 위해 삭제
        # 앞에서 부터 지워지면 리스트가 앞당겨져서 오류가 일어나기때문에 reverse해주고 지워준다.
        d_list.reverse()
        for d in d_list:
            del Util.a_list[d]
            # 외계인이 화면 밖으로 나간 횟수
            Util.loss += Util.obj_num

        dm_list = []
        da_list = []

        for i in range(len(Util.m_list)):
            for j in range(len(Util.a_list)):
                m = Util.m_list[i]
                a = Util.a_list[j]
                if crash(m,a) is True:
                    dm_list.append(i)
                    da_list.append(j)
        
        # 미사일2개와 외계인 1개가 같이 만나는 경우가 있을 수도 있으니까 배제하기위해 중복제거를 해준다.
        dm_list = list(set(dm_list))
        da_list = list(set(da_list))
        # reverse 하지않고 지우면 앞에서 부터 지워지고 앞에서부터지워지면 index의 변화가 일어나서 reverse를 해야함
        dm_list.reverse()
        da_list.reverse()


        # del로 미사일과 외계인 삭제하기
        try:
            for dm in dm_list:
                del Util.m_list[dm]
        except :
            pass
        try:
            for da in da_list:
                del Util.a_list[da]
                # 피사체 사망시 효과음
                penguin.play()
                # 피사체를 파괴한 횟수
                Util.kill += Util.obj_num
        except :
            pass

    
        for i in range(len(Util.a_list)):
            a = Util.a_list[i]
            # 만약 외계인이 ss 와 부딛치면 게임 종료
            if crash2(a,ss) is True:
                # 부딛칠 때 효과음
                boom1.play()
                game_over.play()

                # 1초뒤에 꺼지도록 함
                time.sleep(Util.sleep_time)
                # while 문이 종료되도록 하는 key
                SB = True
                # Go 가 0 인상태로 while문을 빠져나왔다면 x버튼으로 빠져나온것
                Util.GO = True


        for i in range(len(Util.block_list)):
            b = Util.block_list[i]
            # 만약 장애물과 ss가 부딛치면 게임 종료시킴
            if crash2(b,ss) is True:
                # 부딛칠 때 효과음
                boom1.play()
                game_over.play()
                time.sleep(Util.sleep_time)
                # while문 종료 키 
                SB = True
                Util.GO = True


        # score 가 0 점이 되면 프로그램 종료
        if Util.score < 0:
            SB = True
            Util.GO = True
        


        # 4-4. 그리기 
        #  마우스에의해 창크기가 바뀜에 따라 배경화면 크기가 바뀜
        background_image_desert = pygame.image.load("SourceCode/Image/Antartic.png")
        background_image_desert = pygame.transform.scale(background_image_desert, size)
        screen.blit(background_image_desert, Util.start_loc)
        

        # 비행체 보여주기
        ss.show()
        # 미사일 보여주기
        for m in Util.m_list:
            m.show()
        # 피사체 보여주기
        for a in Util.a_list:
            # print(a.sx,a.sy)
            if (a.sx > Size.err_x) or (a.sy > Size.err_y):
                a.put_img("SourceCode/Image/penguin2-removebg-preview.png")
                a.change_size(Size.standard_size,Size.standard_size)
            a.show()
        # 선인장 장애물 보여주기
        for d in Util.block_list:
            d.show()
        # 점수 산정
        # Util.score = (Util.kill*5 - Util.loss*8)
        # 점수산정을 메소드화 하였음
        cal_score(Util.kill, Util.loss)
        
        font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf", FontSize.size_kill_loss)

        text_kill = font.render("Killed : {} Loss : {}  Score : {} HighScore : {}".format(Util.kill, Util.loss, Util.score, Util.highscore), True, Color.yellow) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔

        screen.blit(text_kill,FontSize.loc_kill_loss) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
        
        # 현재 흘러간 시간
        text_time = font.render("Time : {:.2f}".format(delta_time), True, Color.purple)
        screen.blit(text_time,(size[0]-FontSize.len_for_time, FontSize.len_for_time_ysize))
        
        # 4-5. 업데이트
        pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨
        Move.position = True
        

# 5. 게임종료(1. x키를 눌러서 게임이 종료된 경우, 2. 죽어서 게임이 종료된 경우)
# 이건 게임오버가 된 상황! 게임 오버 음악 스타트
game_over.play()
while Util.GO:
    for event in pygame.event.get(): # 이벤트가 있다면
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
               restart() 
        if event.type == pygame.QUIT:
            Util.GO = False
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            Size.x_resize_rate = width / size[Size.x]
            Size.y_resize_rate = height / size[Size.y]
            size =[width, height]
            window = pygame.display.set_mode(size, pygame.RESIZABLE)
            Move.position = True
    # 최고기록 수정
    if Util.score > Util.highscore:
        d = open('Icescore.txt', 'w')
        d.write(str(Util.score))
        d.close()


    background_image_desert = pygame.transform.scale(background_image_desert, size)
    screen.blit(background_image_desert, Util.start_loc)

    FontSize.size_gameover = sum(size) // Resizing.size_gameover
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf", FontSize.size_gameover)
    Rfont = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf", FontSize.size_restart)
    text_kill = font.render("GAME OVER", True, Color.red) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    text_restart = Rfont.render("Restart >> Press R", True, Color.yellow)
    # screen.blit(text_kill,(size[0] // Size.half_split_num - (size[0] // Size.half_split_num) // Size.half_split_num + FontSize.lensize_gameover, round((size[1] / Size.half_split_num) - FontSize.lensize_gameover))) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    screen.blit(text_kill, (size[Size.x] * Size.three_five - FontSize.size_gameover, size[Size.x]//Size.half_split_num ))
    screen.blit(text_restart, (Size.restart_middle, size[Size.y]//Size.half_split_num ))
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨
    Move.position = False

pygame.quit()
