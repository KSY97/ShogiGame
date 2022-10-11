# 장기판 규격 800,630
# 총프레임 860,690
# 여백 30
# 돌 이미지 크기 70x70
# (마상마상:0, 마상상마:1, 상마상마:2,상마마상,3)
# 선수 : 초, 후 수: 한


import tkinter as tk 
from PIL import Image, ImageTk
from sample_1 import State 
from pathlib import Path


class GameUI(tk.Frame): # 클래스는 보통 부모클래스가 뭔지를 넣는다.
    # __init__ 부분에서는 게임 상태와 PV MCTS로 행동 선택을 수행하는 함수와
    # 이미지 캔버스를 준비한다. 마지막으로 화면을 갱신하고, 초기화면을 표시한다.
    def __init__(self, idx, master=None):
        tk.Frame.__init__(self,master)
        # 타이틀 표시
        self.master.title("shogi.")
        print("idx = ",idx)

        # 게임 상태 생성
        # self.state = State()

        # PV MCTS를 활용한 행동 선택을 따르는 함수 생성
        # self.next_action = pv_mcts_action(model, 0.0)
    #    dxy = [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7], [0, -8], # 0-8  차,졸,포,사,왕
    #           [0, -9], 
    #           [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0],                  # 9-16
    #           [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9],          # 17-25
    #           [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0], [-8, 0],          # 26-33
    #           [1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2],          # 34-41  마
    #           [2, -3], [3, -2], [3, 2], [2, 3], [-2, 3], [-3, 2], [-3, -2], [-2, -3]]          # 42-49  상

        
        # 이미지 로드
        # self.cho_images = []
        # self.han_images = []
        self.cho_images = []
        self.han_images = []
        
        # 초 돌 (1:초차,2:초졸,3:초마,4:초포,5:초사,6:초상,7:초왕)
        self.cho_images.append(0) # API와 idx 번호를 일치시키기 위해
        self.cho_images.append(ImageTk.PhotoImage(Image.open("chocha.png")))
        self.cho_images.append(ImageTk.PhotoImage(Image.open("chojol.png")))
        self.cho_images.append(ImageTk.PhotoImage(Image.open("choma.png")))
        self.cho_images.append(ImageTk.PhotoImage(Image.open("chopo.png")))
        self.cho_images.append(ImageTk.PhotoImage(Image.open("chosa.png")))
        self.cho_images.append(ImageTk.PhotoImage(Image.open("chosang.png")))
        self.cho_images.append(ImageTk.PhotoImage(Image.open("chowang.png"))) 

        # 한 돌 (1:한차,2:한졸,3:한마,4:한포,5:한사,6:한상,7:한왕)
        self.han_images.append(0) # API와 idx 번호를 일치시키기 위해
        self.han_images.append(ImageTk.PhotoImage(Image.open("hancha.png")))
        self.han_images.append(ImageTk.PhotoImage(Image.open("hanjol.png")))
        self.han_images.append(ImageTk.PhotoImage(Image.open("hanma.png")))
        self.han_images.append(ImageTk.PhotoImage(Image.open("hanpo.png")))
        self.han_images.append(ImageTk.PhotoImage(Image.open("hansa.png")))
        self.han_images.append(ImageTk.PhotoImage(Image.open("hansang.png")))
        self.han_images.append(ImageTk.PhotoImage(Image.open("hanwang.png")))

        
        #캔버스 생성
        self.c = tk.Canvas(self, width=860,height=690,highlightthickness = 0)
        # self.c.bind(<"Button-1">,turn_of_human) # 클릭 판정 추가
        self.c.pack()

        # 그림 갱신
        self.on_draw() 

        
        self.idx = idx
        self.state = State(idx = self.idx)


        def turn_of_human(self, event):
            self.idx = idx
            if slef.state.is_done(): # 게임 종료시
                self.state = State(idx = self.idx)
                self.on_draw()  # 게임을 초기상태로 돌린다.
                return
            
            if not self.state.is_first_player(): # 선수가 아닐경우
                return # 그냥 패스

            # 말 선택과 이동 위치 계산
            


        # 내가 선일때 말 배치
         # 3:초마,6:초상
        if self.idx[1] == 0:
            self.a,self.b,self.d,self.e = 3,6,3,6 # 마상마상
            self.my_batch()
        if self.idx[1] == 1:
            self.a,self.b,self.d,self.e = 3,6,6,3 # 마상상마
            self.my_batch()
        if self.idx[1] == 2:
            self.a,self.b,self.d,self.e = 6,3,6,3 # 상마상마
            self.my_batch()
        if self.idx[1] == 3:
            self.a,self.b,self.d,self.e = 6,3,3,6 # 상마마상
            self.my_batch()


        # 내가 후 일때 말 배치
        # 3:초마,6:초상
        if self.idx[1] == 0:
            self.a,self.b,self.d,self.e = 3,6,3,6 # 마상마상
            self.enemy_batch()
        if self.idx[1] == 1:
            self.a,self.b,self.d,self.e = 3,6,6,3 # 마상상마
            self.enemy_batch()
        if self.idx[1] == 2:
            self.a,self.b,self.d,self.e = 6,3,6,3 # 상마상마
            self.enemy_batch()
        if self.idx[1] == 3:
            self.a,self.b,self.d,self.e = 6,3,3,6 # 상마마상
            self.enemy_batch()



    def on_draw(self): # 그림 갱신
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 860, 690, width=0.0, fill='#EDAA56') # 외각 사각형
        self.c.create_rectangle(30, 30, 830, 660, outline='black',width=1.0, fill='#EDAA56') # 장기판 사각형
        
        #가로줄 그리기
        for i in range(1,8): 
            self.c.create_line(i*100+30,0+30,i*100+30,630+30,fill="#000000")
        #세로줄 그리기
        for i in range(9):
            self.c.create_line(0+30,i*70+30,800+30,i*70+30,fill="#000000")
        # 왕 x자 그리기(상대편 꺼)
        self.c.create_line(330,30,530,170,width=1.0,fill="#000000")
        self.c.create_line(330,170,530,30,width=1.0,fill="#000000")
        # 왕 x자 그리기(내 꺼)
        self.c.create_line(330,660,530,520,width=1.0,fill="#000000")
        self.c.create_line(330,520,530,660,width=1.0,fill="#000000")
        # 점 그리기 (상대꺼)
        self.c.create_oval(30,240,30,240,width=6.0,fill="#000000")
        self.c.create_oval(130,170,130,170,width=6.0,fill="#000000")
        self.c.create_oval(230,240,230,240,width=6.0,fill="#000000")
        self.c.create_oval(430,240,430,240,width=6.0,fill="#000000")
        self.c.create_oval(630,240,630,240,width=6.0,fill="#000000")
        self.c.create_oval(730,170,730,170,width=6.0,fill="#000000")
        self.c.create_oval(830,240,830,240,width=6.0,fill="#000000")
        # 점 그리기 (내꺼)
        self.c.create_oval(30,450,30,450,width=6.0,fill="#000000")
        self.c.create_oval(130,520,130,520,width=6.0,fill="#000000")
        self.c.create_oval(230,450,230,450,width=6.0,fill="#000000")
        self.c.create_oval(430,450,430,450,width=6.0,fill="#000000")
        self.c.create_oval(630,450,630,450,width=6.0,fill="#000000")
        self.c.create_oval(730,520,730,520,width=6.0,fill="#000000")
        self.c.create_oval(830,450,830,450,width=6.0,fill="#000000")
        
        
      
    # 한 돌 (1:한차,2:한졸,3:한마,4:한포,5:한사,6:한상,7:한왕)
    def enemy_batch(self):
        if self.idx[0] == 0:
            images = self.han_images
        elif self.idx[0] == 1:
            images = self.cho_images
        
        self.c.create_image(30,30,image=images[1]) # 한 차
        self.c.create_image(130,30,image=images[self.e]) # 한 마
        self.c.create_image(230,30,image=images[self.d]) # 한 상
        self.c.create_image(330,30,image=images[5]) # 한 사
        self.c.create_image(530,30,image=images[5]) # 한 사
        self.c.create_image(630,30,image=images[self.b])# 한 상
        self.c.create_image(730,30,image=images[self.a])# 한 마
        self.c.create_image(830,30,image=images[1])# 한 차
        self.c.create_image(430,100,image=images[7]) # 한 왕
        self.c.create_image(130,170,image=images[4]) # 한 포
        self.c.create_image(730,170,image=images[4]) # 한 포

        # 한 졸 그리기
        for i in range(5):
            self.c.create_image(i*200+30,240,image=images[2])
    
    # # 한 돌 상마상마
    # def han_sangmamasang(self):
    #     self.c.create_image(30,30,image=self.images[7]) # 한 차
    #     self.c.create_image(130,30,image=self.images[9]) # 한 마
    #     self.c.create_image(230,30,image=self.images[12]) # 한 상
    #     self.c.create_image(330,30,image=self.images[11]) # 한 사
    #     self.c.create_image(530,30,image=self.images[11]) # 한 사
    #     self.c.create_image(630,30,image=self.images[12])# 한 상
    #     self.c.create_image(730,30,image=self.images[9])# 한 마
    #     self.c.create_image(830,30,image=self.images[7])# 한 차
    #     self.c.create_image(430,100,image=self.images[13]) # 한 왕
    #     self.c.create_image(130,170,image=self.images[10]) # 한 포
    #     self.c.create_image(730,170,image=self.images[10]) # 한 포

    #     # 한 졸 그리기
    #     for i in range(5):
    #         self.c.create_image(i*200+30,240,image=self.images[8])
    
    # def han_sangmamasang(self):
    #     self.c.create_image(30,30,image=self.images[7]) # 한 차
    #     self.c.create_image(130,30,image=self.images[9]) # 한 마
    #     self.c.create_image(230,30,image=self.images[12]) # 한 상
    #     self.c.create_image(330,30,image=self.images[11]) # 한 사
    #     self.c.create_image(530,30,image=self.images[11]) # 한 사
    #     self.c.create_image(630,30,image=self.images[12])# 한 상
    #     self.c.create_image(730,30,image=self.images[9])# 한 마
    #     self.c.create_image(830,30,image=self.images[7])# 한 차
    #     self.c.create_image(430,100,image=self.images[13]) # 한 왕
    #     self.c.create_image(130,170,image=self.images[10]) # 한 포
    #     self.c.create_image(730,170,image=self.images[10]) # 한 포

    #     # 한 졸 그리기
    #     for i in range(5):
    #         self.c.create_image(i*200+30,240,image=self.images[8])

    # def han_sangmamasang(self):
    #     self.c.create_image(30,30,image=self.images[7]) # 한 차
    #     self.c.create_image(130,30,image=self.images[9]) # 한 마
    #     self.c.create_image(230,30,image=self.images[12]) # 한 상
    #     self.c.create_image(330,30,image=self.images[11]) # 한 사
    #     self.c.create_image(530,30,image=self.images[11]) # 한 사
    #     self.c.create_image(630,30,image=self.images[12])# 한 상
    #     self.c.create_image(730,30,image=self.images[9])# 한 마
    #     self.c.create_image(830,30,image=self.images[7])# 한 차
    #     self.c.create_image(430,100,image=self.images[13]) # 한 왕
    #     self.c.create_image(130,170,image=self.images[10]) # 한 포
    #     self.c.create_image(730,170,image=self.images[10]) # 한 포

    #     # 한 졸 그리기
    #     for i in range(5):
    #         self.c.create_image(i*200+30,240,image=self.images[8])
    
        
    def my_batch(self):
         # 초 돌 (1:초차,2:초졸,3:초마,4:초포,5:초사,6:초상,7:초왕)
         # 한 돌 (1:한차,2:한졸,3:한마,4:한포,5:한사,6:한상,7:한왕)
        if self.idx[0] == 0:
            images = self.cho_images
        elif self.idx[0] == 1:
            images = self.han_images

        self.c.create_image(30,660,image=images[1]) # 초 차
        self.c.create_image(130,660,image=images[self.a]) # 초 마
        self.c.create_image(230,660,image=images[self.b]) # 초 상
        self.c.create_image(330,660,image=images[5]) # 초 사
        self.c.create_image(530,660,image=images[5]) # 초 사
        self.c.create_image(630,660,image=images[self.d]) # 초 마
        self.c.create_image(730,660,image=images[self.e]) # 초 상
        self.c.create_image(830,660,image=images[1]) # 초 차
        self.c.create_image(430,590,image=images[7]) # 초 왕
        self.c.create_image(130,520,image=images[4]) # 초 포
        self.c.create_image(730,520,image=images[4]) # 초 포

        for i in range(5):
            self.c.create_image(i*200+30,450,image=images[2]) # 초 졸


    
    # # 돌배치 선택
    # if self.idx == 0:
    #         self.masangmasang()
    # if self.idx == 1:
    #         self.sangmasangma()
    # if self.idx == 2:
    #         self.masangsangma()
    # if self.idx == 3:
    #         self.sangmamasang()
    # if self.idx == None:
    #     print('None')
     
        
        
# f = GameUI(idx=1)
# f.pack()
# f.mainloop()

