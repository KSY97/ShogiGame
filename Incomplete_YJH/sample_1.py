
# 패키지 임포트
import random
import math

# 게임 상태
class State:
    # 초기화
    def __init__(self, pieces=None, enemy_pieces=None, depth=0,idx=None): # depth는 현재 누구 턴인지를 표시한다.
        # 방향 정수
        # self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

        # 말의 배치
        self.pieces = pieces if pieces != None else [0] * (9*10) # 초기 말 배치
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * (9*10)
        self.depth = depth
        

        self.idx = idx ## 스테이트 안에서 사용할 수 있는 전역변수 생성


        # 말의 초기 배치 (적 돌과 내돌의 배치 경우 4가지를 고려 해야한다.
        #                 각각 마상마상,상마상마,마상상마,상마마상)
        # 차 : 1, 졸: 2, 마: 3, 포: 4, 사: 5, 상: 6, 왕: 7

        if pieces == None or enemy_pieces == None:
            if self.idx[0] == 0:
              a, b, c, d = 3, 6, 3, 6 # 마상마상
            elif self.idx[0] == 1:
              a, b, c, d = 3, 6, 6, 3 # 마상상마
            elif self.idx[0] == 2:
              a, b, c, d = 6, 3, 6, 3 # 상마상마
            elif self.idx[0] == 3:
              a, b, c, d = 6, 3, 3, 6 # 상마마상
            
            if self.idx[1] == 0:
              e, f, g, h = 3, 6, 3, 6 # 마상마상
            elif self.idx[1] == 1:
              e, f, g, h = 3, 6, 6, 3 # 마상상마
            elif self.idx[1] == 2:
              e, f, g, h = 6, 3, 6, 3 # 상마상마
            elif self.idx[1] == 3:
              e, f, g, h = 6, 3, 3, 6 # 상마마상
                          



            self.pieces =  [0,0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,0,
                            0,0,0,0,0,0,0,0,0,
                            2,0,2,0,2,0,2,0,2,
                            0,4,0,0,0,0,0,4,0,
                            0,0,0,0,7,0,0,0,0,
                            1,a,b,5,0,5,c,d,1]
                
            self.enemy_pieces =  [0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,
                                  2,0,2,0,2,0,2,0,2,
                                  0,4,0,0,0,0,0,4,0,
                                  0,0,0,0,7,0,0,0,0,
                                  1,e,f,5,0,5,g,h,1]
        print(self.pieces)
        print(self.enemy_pieces)