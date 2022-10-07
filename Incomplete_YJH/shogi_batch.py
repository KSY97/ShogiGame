# 장기판 규격 800,630
# 총프레임 860,690
# 여백 30
# 돌 이미지 크기 70x70
import tkinter as tk 
from PIL import Image, ImageTk
from sample_1 import State 

class GameUI(tk.Frame): # 클래스는 보통 부모클래스가 뭔지를 넣는다.
    def __init__(self, idx, master=None):
        tk.Frame.__init__(self,master)
        # 타이틀 표시
        self.master.title("shogi.")
        
        
        # 이미지 로드
        # image = Image.open("testimo.png")
        self.images = []
        # 초 돌 (0:초차,1:초졸,2:초마,3:초포,4:초사,5:초상,6:초왕)
        self.images.append(ImageTk.PhotoImage(Image.open("chocha.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("chojol.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("choma.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("chopo.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("chosa.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("chosang.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("chowang.png"))) 

        # 한 돌 (7:한차,8:한졸,9:한마,10:한포,11:한사,12:한상,13:한왕)
        self.images.append(ImageTk.PhotoImage(Image.open("hancha.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("hanjol.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("hanma.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("hanpo.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("hansa.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("hansang.png")))
        self.images.append(ImageTk.PhotoImage(Image.open("hanwang.png")))

        

        #캔버스 생성
        self.c = tk.Canvas(self, width=860,height=690,highlightthickness = 0)
        self.c.pack()

        #그림 갱신
        self.on_draw()

        self.idx = idx
        self.state = State(idx = self.idx)

        # 돌배치 선택
        if self.idx[0] == 0:
             self.masangmasang()
        if self.idx[0] == 1:
             self.sangmasangma()
        if self.idx[0] == 2:
             self.masangsangma()
        if self.idx[0] == 3:
             self.sangmamasang()
        if self.idx[0] == None:
            print('None')


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
        
        
        # 한 돌 (7:한차,8:한졸,9:한마,10:한포,11:한사,12:한상,13:한왕)
        # 초 돌 (0:초차,1:초졸,2:초마,3:초포,4:초사,5:초상,6:초왕)
        # self.c.create_image(100,70,image=self.images[0],anchor=tk.NW)
        
        # 한 돌 셋팅

        self.c.create_image(0,0,image=self.images[7],anchor=tk.NW) # 한 차
        self.c.create_image(100,0,image=self.images[9],anchor=tk.NW) # 한 마
        self.c.create_image(200,0,image=self.images[12],anchor=tk.NW) # 한 상
        self.c.create_image(300,0,image=self.images[11],anchor=tk.NW) # 한 사
        self.c.create_image(500,0,image=self.images[11],anchor=tk.NW) # 한 사
        self.c.create_image(600,0,image=self.images[12],anchor=tk.NW)# 한 상
        self.c.create_image(700,0,image=self.images[9],anchor=tk.NW)# 한 마
        self.c.create_image(800,0,image=self.images[7],anchor=tk.NW)# 한 차
        self.c.create_image(400,70,image=self.images[13],anchor=tk.NW) # 한 왕
        self.c.create_image(100,140,image=self.images[10],anchor=tk.NW) # 한 포
        self.c.create_image(700,140,image=self.images[10],anchor=tk.NW) # 한 포

         # 한 졸 그리기
        for i in range(5):
            self.c.create_image(i*200,210,image=self.images[8],anchor=tk.NW)
        
        
    def sangmamasang(self):
        # 초 돌 셋팅 : 초 돌 (0:초차,1:초졸,2:초마,3:초포,4:초사,5:초상,6:초왕)
        self.c.create_image(0,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(100,630,image=self.images[5],anchor=tk.NW) # 초 상
        self.c.create_image(200,630,image=self.images[2],anchor=tk.NW) # 초 마
        self.c.create_image(300,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(500,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(600,630,image=self.images[2],anchor=tk.NW) # 초 마
        self.c.create_image(700,630,image=self.images[5],anchor=tk.NW) # 초 상
        self.c.create_image(800,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(400,560,image=self.images[6],anchor=tk.NW) # 초 왕
        self.c.create_image(100,490,image=self.images[3],anchor=tk.NW) # 초 포
        self.c.create_image(700,490,image=self.images[3],anchor=tk.NW) # 초 포

        for i in range(5):
            self.c.create_image(i*200,420,image=self.images[1],anchor=tk.NW) # 초 졸

    def masangmasang(self):
        # 초 돌 셋팅 : 초 돌 (0:초차,1:초졸,2:초마,3:초포,4:초사,5:초상,6:초왕)
        self.c.create_image(0,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(100,630,image=self.images[2],anchor=tk.NW) # 초 마
        self.c.create_image(200,630,image=self.images[5],anchor=tk.NW) # 초 상
        self.c.create_image(300,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(500,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(600,630,image=self.images[2],anchor=tk.NW) # 초 마
        self.c.create_image(700,630,image=self.images[5],anchor=tk.NW) # 초 상
        self.c.create_image(800,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(400,560,image=self.images[6],anchor=tk.NW) # 초 왕
        self.c.create_image(100,490,image=self.images[3],anchor=tk.NW) # 초 포
        self.c.create_image(700,490,image=self.images[3],anchor=tk.NW) # 초 포

        for i in range(5):
            self.c.create_image(i*200,420,image=self.images[1],anchor=tk.NW) # 초 졸

    def sangmasangma(self):
        # 초 돌 셋팅 : 초 돌 (0:초차,1:초졸,2:초마,3:초포,4:초사,5:초상,6:초왕)
        self.c.create_image(0,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(100,630,image=self.images[5],anchor=tk.NW) # 초 상
        self.c.create_image(200,630,image=self.images[2],anchor=tk.NW) # 초 마
        self.c.create_image(300,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(500,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(600,630,image=self.images[5],anchor=tk.NW) # 초 마
        self.c.create_image(700,630,image=self.images[2],anchor=tk.NW) # 초 상
        self.c.create_image(800,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(400,560,image=self.images[6],anchor=tk.NW) # 초 왕
        self.c.create_image(100,490,image=self.images[3],anchor=tk.NW) # 초 포
        self.c.create_image(700,490,image=self.images[3],anchor=tk.NW) # 초 포

        for i in range(5):
            self.c.create_image(i*200,420,image=self.images[1],anchor=tk.NW) # 초 졸
    

    def masangsangma(self):
        # 초 돌 셋팅 : 초 돌 (0:초차,1:초졸,2:초마,3:초포,4:초사,5:초상,6:초왕)
        self.c.create_image(0,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(100,630,image=self.images[2],anchor=tk.NW) # 초 마
        self.c.create_image(200,630,image=self.images[5],anchor=tk.NW) # 초 상
        self.c.create_image(300,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(500,630,image=self.images[4],anchor=tk.NW) # 초 사
        self.c.create_image(600,630,image=self.images[2],anchor=tk.NW) # 초 상
        self.c.create_image(700,630,image=self.images[5],anchor=tk.NW) # 초 마
        self.c.create_image(800,630,image=self.images[0],anchor=tk.NW) # 초 차
        self.c.create_image(400,560,image=self.images[6],anchor=tk.NW) # 초 왕
        self.c.create_image(100,490,image=self.images[3],anchor=tk.NW) # 초 포
        self.c.create_image(700,490,image=self.images[3],anchor=tk.NW) # 초 포

        for i in range(5):
            self.c.create_image(i*200,420,image=self.images[1],anchor=tk.NW) # 초 졸
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

