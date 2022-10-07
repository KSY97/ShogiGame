import tkinter as tk 
# from shogi_game import GameUI
from shogi_batch import GameUI
from PIL import Image, ImageTk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None # 지금 화면이 출력되는 것

        self.idx_list = []

        self.switch_frame(StartPage)
        self.batch = None
        
        

    def switch_frame(self, frame_class, idx = None):
        idx_list = self.idx_list

        if idx != None:  # idx가 있을 경우 (장기판을 띄우는 경우)
    
            if len(idx_list) == 1:
                self.idx_list.append(idx)
                idx_list = self.idx_list
                new_frame = frame_class(idx = idx_list)
            else:
                self.idx_list.append(idx)
                new_frame = frame_class(self)
        else:            # idx가 없을 경우인데 (장기판을 띄우지 않는 모든 경우)
            self.idx_list = []
            new_frame = frame_class(self)
            

        if self._frame is not None: ## 클릭했을때
            self._frame.destroy() ## 기존창 파괴
            
        self._frame = new_frame ## 새창을 self._frame에 넣어주고
        self._frame.pack() ## pack으로 실행
        

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="AI_shogi", font=('Helvetica', 32, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="선 수",font=('Helvetica', 18, "bold"),
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="후 수",font=('Helvetica', 18, "bold"),
                  command=lambda: master.switch_frame(PageOne)).pack()

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='green')
        tk.Label(self, text="선수 말배치 결정", font=('Helvetica', 32, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="마상마상",
                  command=lambda: master.switch_frame(PageTwo, 0)).pack()
        tk.Button(self, text="마상상마",
                  command=lambda: master.switch_frame(PageTwo, 1)).pack()
        tk.Button(self, text="상마상마",
                  command=lambda: master.switch_frame(PageTwo, 2)).pack()
        tk.Button(self, text="상마마상",
                  command=lambda: master.switch_frame(PageTwo, 3)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="후수 말배치 결정", font=('Helvetica', 32, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="마상마상",
                  command=lambda: master.switch_frame(GameUI, 0)).pack()
        tk.Button(self, text="마상상마",
                  command=lambda: master.switch_frame(GameUI, 1)).pack()
        tk.Button(self, text="상마상마",
                  command=lambda: master.switch_frame(GameUI, 2)).pack()
        tk.Button(self, text="상마마상",
                  command=lambda: master.switch_frame(GameUI, 3)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()