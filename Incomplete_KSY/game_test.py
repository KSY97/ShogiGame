
# 패키지 임포트
import random
import math

# 최대 둘수 있는 수
MAX_DEPTH = 200

# 게임 상태
class State:
    # 초기화
    def __init__(self, pieces=None, enemy_pieces=None, depth=0,idx=None): # depth는 현재 누구 턴인지를 표시한다.
        # 방향 정수
        # 순서 -> 상우하좌                                                                         #인덱스
        self.dxy = [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7], [0, -8], [0, -9], # 0-8  차,졸,포,사,왕
            [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0],                  # 9-16
            [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9],          # 17-25
            [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0], [-8, 0],          # 26-33
            [1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2],          # 34-41  마
            [2, -3], [3, -2], [3, 2], [2, 3], [-2, 3], [-3, 2], [-3, -2], [-2, -3],          # 42-49  상
            [1, -1], [2, -2], [1, 1], [2, 2], [-1, 1], [-2, 2], [-1, -1], [-2, -2]]          # 50-57 궁성안의 대각선 움직임

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
            if self.idx == None: # 인덱스 설정을 하지 않는 기본값
              a, b, c, d = 3, 6, 3, 6 # 마상마상
            elif self.idx[0] == 0:
              a, b, c, d = 3, 6, 3, 6 # 마상마상
            elif self.idx[0] == 1:
              a, b, c, d = 3, 6, 6, 3 # 마상상마
            elif self.idx[0] == 2:
              a, b, c, d = 6, 3, 6, 3 # 상마상마
            elif self.idx[0] == 3:
              a, b, c, d = 6, 3, 3, 6 # 상마마상
            
            if self.idx == None: # 인덱스 설정을 하지 않는 기본값
              e, f, g, h = 3, 6, 3, 6 # 마상마상
            elif self.idx[1] == 0:
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
        # print(self.pieces)
        # print(self.enemy_pieces)

    # 패배 여부 판정
    def is_lose(self):
      if self.is_draw():
          if self.cal_piece_score() > self.cal_enemy_piece_score():
            return False
          else:
            return True
      else:
        for i in range(90):
            if self.pieces[i] == 7:  # 왕이 존재한다면
                return False
        return True
        # # 본인의 점수가 10점보다 적다면 게임 끝(패배)
        # if playerScore<10:
        #   return True

    # 200턴안에 안끝나면 종료
    def is_draw(self):
        return self.depth >= MAX_DEPTH  # 200수 안에 안끝난다면

    # 게임 종료 여부 판정
    def is_done(self):
        return self.is_lose()
    
    # 기물 점수 계산
    # 차(1):13점, 졸(2):2점, 마(3):5점, 포(4):7점, 사(5):3점, 상(6):3점, 왕(7):0점
    def cal_piece_score(self):
      temp_list = [0] * 8
      score = 0
      for i in range(90):
        temp_list[self.pieces[i]] += 1
      
      # 왕의 점수 계산 X
      for i in range(1, 7):
        if i == 1:
          score += (13*temp_list[i])
        elif i == 2:
          score += (2*temp_list[i])
        elif i == 3:
          score += (5*temp_list[i])
        elif i == 4:
          score += (7*temp_list[i])
        elif i == 5 or i == 6:
          score += (3*temp_list[i])

      if not self.is_first_player():
        return score + 1.5
      return score

    def cal_enemy_piece_score(self):
      temp_list = [0] * 8
      score = 0
      for i in range(90):
        temp_list[self.enemy_pieces[i]] += 1
      
      # 왕의 점수 계산 X
      for i in range(1, 7):
        if i == 1:
          score += (13*temp_list[i])
        elif i == 2:
          score += (2*temp_list[i])
        elif i == 3:
          score += (5*temp_list[i])
        elif i == 4:
          score += (7*temp_list[i])
        elif i == 5 or i == 6:
          score += (3*temp_list[i])
      
      if not self.is_first_player():
        return score
      return score + 1.5
    
    # 듀얼 네트워크 입력 2차원 배열 얻기
    def pieces_array(self):
      # 플레이어 별 듀얼 네트워크 입력 1차원 배열 얻기
      def pieces_array_of(pieces):
        table_list = []
        # 1: 차, 2: 졸, 3: 마, 4: 포, 5: 사, 6: 상, 7: 왕
        for j in range(1, 8):
          table = [0] * 90
          table_list.append(table)
          for i in range(90):
            if pieces[i] == j:
              table[i] = 1
        return table_list
        
      # 듀얼 네트워크 입력 2차원 배열 반환
      return [pieces_array_of(self.pieces), pieces_array_of(self.enemy_pieces)]

    def is_first_player(self):
      return self.depth % 2 == 0

    # 말의 이동 도착 위치 및 이동 시작 위치를 행동으로 변환                                                                        
    def position_to_action(self, position, direction):
      return position * 58 + direction

    # 행동을 말의 이동 도착 위치 및 이동 시작 위치로 변환
    def action_to_position(self, action):
        return (int(action / 58), action % 58)

    # 가능한 행동 함수
    def legal_actions(self):
      actions = []
      for p in range(90):
        if self.pieces[p] != 0:
          actions.extend(self.legal_actions_pos(p))
      return actions 

    # 각 기물들의 모든 이동가능한 방향 함수
    def legal_actions_pos(self, position_src):
      # 말이 이동 가능한 방향
      piece_type = self.pieces[position_src]
      if piece_type == 1: # 차
        directions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                      18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
        return self.illegal_actions(directions, position_src)
      
      elif piece_type == 2: #졸
        directions = [0, 9, 26, 50, 56]
        return self.illegal_actions(directions, position_src)
      
      elif piece_type == 3: #마
        directions = [34, 35, 36, 37, 38, 39, 40, 41]
        return self.illegal_actions(directions, position_src)
      
      elif piece_type == 4: #포
        directions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                  18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
        return self.illegal_actions(directions, position_src)
      
      elif piece_type == 5: #사
        directions = [0, 9, 17, 26, 50, 52, 54, 56]
        return self.illegal_actions(directions, position_src)
      
      elif piece_type == 6: #상
        directions = [42, 43, 44, 45, 46, 47, 48, 49]
        return self.illegal_actions(directions, position_src)
      
      elif piece_type == 7: #왕
        directions = [0, 9, 17, 26, 50, 52, 54, 56]
        return self.illegal_actions(directions, position_src)

    # 행동할 수 없는 수 걸러주는 함수
    def illegal_actions(self, directions, position_src): 
      actions = []
      dierction = []

      # 말의 이동 전 위치 좌표 얻기
      bef_x = position_src % 9
      bef_y = int(position_src / 9)

      # 합법적인 수 얻기
      for direction in directions:
        
        # 말의 이동 후 위치
        x = position_src % 9 + self.dxy[direction][0] # 방향정수의 x축
        y = int(position_src / 9) + self.dxy[direction][1] # 방향정수의 y축
        p = x + y * 9 # 9진수 화 


        # 이동이 불가능 한 수들 걸러내기

        # 이동한 후의 위치가 보드판의 범위를 벗어나지 않았을 때
        if 0 <= x and x <= 8 and 0 <= y and y <= 9 and self.pieces[p] == 0: 
      
          # 이동경로가 막혀 있는 경우

          # 차
          if self.pieces[position_src] == 1:
            # 우
            if self.dxy[direction][0] > 0 and self.dxy[direction][1] == 0:
              for path in range(1, self.dxy[direction][0]):
                if self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 0: # 상대편 보드에 기물이 있다면 행동추가 하고 break 
                  actions.append(self.position_to_action(p, direction))
                  break
                elif self.pieces[(bef_x + path) + bef_y * 9] != 0: # 내 보드에 기물이 있다면 그냥 break
                  break
                else:
                  actions.append(self.position_to_action(p, direction)) # 둘다 아닐 경우 행동추가
            # 좌
            if self.dxy[direction][0] < 0 and self.dxy[direction][1] == 0:
              for n_path in range(-1, self.dxy[direction][0], -1):
                if self.enemy_pieces[89 - ((bef_x + n_path) + bef_y * 9)] != 0:
                  actions.append(self.position_to_action(p, direction))
                  break
                elif self.pieces[(bef_x + n_path) + bef_y * 9] != 0:
                  break
                else:
                  actions.append(self.position_to_action(p, direction))
            # 하
            if self.dxy[direction][1] > 0 and self.dxy[direction][0] == 0: 
              for path in range(1, self.dxy[direction][1]):
                if self.enemy_pieces[89 - (bef_x + (bef_y+ path) * 9)] != 0:
                  actions.append(self.position_to_action(p, direction))
                  break
                elif self.pieces[bef_x + (bef_y+ path) * 9] != 0:
                  break
                else:
                  actions.append(self.position_to_action(p, direction))
            # 상
            if self.dxy[direction][1] < 0 and self.dxy[direction][0] == 0: 
              for n_path in range(-1, self.dxy[direction][0], -1):
                if self.enemy_pieces[89 - (bef_x + (bef_y+ path) * 9)] != 0:
                  actions.append(self.position_to_action(p, direction))
                  break
                elif self.pieces[bef_x + (bef_y+ path) * 9] != 0:
                  break
                else:
                  actions.append(self.position_to_action(p, direction))
            # 궁성안에 기물이 있을 때 대각선 행동 추가
            if self.dxy[direction][1] != 0 and self.dxy[direction][0] != 0:
              if position_src == 68 or position_src == 5:
                if (self.dxy[direction][1] == -1 and self.dxy[direction][0] == 1) or (self.dxy[direction][1] == -2 and dxy[direction][0] == 2):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 86 or position_src == 23:
                if (self.dxy[direction][1] == -1 and self.dxy[direction][0] == -1) or (self.dxy[direction][1] == -2 and dxy[direction][0] == -2):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 84 or position_src == 21:
                if (self.dxy[direction][1] == 1 and self.dxy[direction][0] == -1) or (self.dxy[direction][1] == 2 and dxy[direction][0] == -2):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 66 or position_src == 3:
                if (self.dxy[direction][1] == 1 and self.dxy[direction][0] == 1) or (self.dxy[direction][1] == 2 and dxy[direction][0] == 2):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 76 or position_src == 13:
                if (self.dxy[direction][1] == 1 and dxy[direction][0] == -1) or (self.dxy[direction][1] == 1 and dxy[direction][0] == 1) or (dxy[direction][1] == -1 and dxy[direction][0] == 1) or (dxy[direction][1] == -1 and dxy[direction][0] == -1):
                  actions.append(self.position_to_action(p, direction))

          #졸
          elif self.pieces[position_src] == 2:
            # 졸이 궁성 안에 없을 때 
            if position_src != 23 or position_src != 21  or  position_src != 66 or position_src != 13:
              actions.append(self.position_to_action(p, direction))
            # 궁성안에 기물이 있을 때 대각선 행동 추가
            if self.dxy[direction][1] != 0 and self.dxy[direction][0] != 0:
              if position_src == 23:
                if (self.dxy[direction][1] == -1 and self.dxy[direction][0] == -1):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 21:
                if (self.dxy[direction][1] == 1 and self.dxy[direction][0] == -1):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 66 or position_src == 3:
                if (self.dxy[direction][1] == 1 and self.dxy[direction][0] == 1) or (self.dxy[direction][1] == 2 and self.dxy[direction][0] == 2):
                  actions.append(self.position_to_action(p, direction))
              if position_src == 13:
                if (self.dxy[direction][1] == 1 and self.dxy[direction][0] == -1) or (self.dxy[direction][1] == -1 and self.dxy[direction][0] == -1):
                  actions.append(self.position_to_action(p, direction))
          
          # 마
          elif self.pieces[position_src] == 3:
            if (bef_x + (bef_y - 1) * 9) <= 89:
              # 상
              if self.pieces[bef_x + (bef_y - 1) * 9] and self.enemy_pieces[89 - (bef_x + (bef_y - 1) * 9)] == 0:
                actions.append(self.position_to_action(p, direction))
            if ((bef_x + 1) + bef_y * 9) <= 89:
              # 우
              if self.pieces[(bef_x + 1) + bef_y * 9] and self.enemy_pieces[89 - ((bef_x + 1) + bef_y * 9)] == 0:
                actions.append(self.position_to_action(p, direction)) 
            if (bef_x + (bef_y + 1) * 9) <= 89:
              # 하
              if self.pieces[bef_x + (bef_y + 1) * 9] and self.enemy_pieces[89 - (bef_x + (bef_y + 1) * 9)] == 0:
                actions.append(self.position_to_action(p, direction))
            if ((bef_x - 1) + bef_y * 9) <= 89:
              # 좌
              if self.pieces[(bef_x - 1) + bef_y * 9] and self.enemy_pieces[89 - ((bef_x - 1) + bef_y * 9)] == 0:
                actions.append(self.position_to_action(p, direction))

          # 포
          elif self.pieces[position_src] == 4:
            # 이동 후의 위치에 적의 포가 없을 때 실행
            if self.enemy_pieces[p] != 4: 
              # x축의 경우
              if self.dxy[direction][0] != 0 and self.dxy[direction][1] == 0:
                # 우
                is_po = False
                for path in range(1, self.dxy[direction][0]):
                  if self.pieces[(bef_x + path) + bef_y * 9] != 0 or self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 0: # 경로 중 뛰어 넘어 갈 기물이 있다면
                    if self.pieces[(bef_x + path) + y * 9] != 4 and self.enemy_pieces[89 - ((bef_x + path) + y * 9)] != 4: # 그 기물이 나 혹은 상대의 포가 아니라면
                      is_po = path + 1
                      break
                if is_po:
                  for path in range(is_po, self.dxy[direction][0]): # 기물을 뛰어 넘은 이후부터 경로를 다시 탐색 
                    if self.enemy_pieces[89 - (bef_x + path) + bef_y * 9] != 0: # 상대편 보드에 기물이 있다면 행동추가 하고 break 
                      actions.append(self.position_to_action(p, direction))
                      break
                    elif self.pieces[(bef_x + path) + bef_y * 9] != 0: # 내 보드에 기물이 있다면 그냥 break
                      break
                    else:
                      actions.append(self.position_to_action(p, direction)) # 둘다 아닐 경우 행동추가
                # 좌
                is_po = False 
                for path in range(-1, self.dxy[direction][0], -1):
                  if self.pieces[(bef_x + path) + bef_y * 9] != 0 or self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 0: # 경로 중 뛰어 넘어 갈 기물이 있다면
                    if self.pieces[(bef_x + path) + bef_y * 9] != 4 and self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 4: # 그 기물이 나 혹은 상대의 포가 아니라면
                      is_po = path - 1
                      break
                if is_po:
                  for path in range(is_po, self.dxy[direction][0], -1): # 기물을 뛰어 넘은 이후부터 경로를 다시 탐색 
                    if self.enemy_pieces[89 - (bef_x + path) + bef_y * 9] != 0: # 상대편 보드에 기물이 있다면 행동추가 하고 break 
                      actions.append(self.position_to_action(p, direction))
                      break
                    elif self.pieces[(bef_x + path) + bef_y * 9] != 0: # 내 보드에 기물이 있다면 그냥 break
                      break
                    else:
                      actions.append(self.position_to_action(p, direction)) # 둘다 아닐 경우 행동추가

              # y축의 경우
              if self.dxy[direction][0] == 0 and self.dxy[direction][1] != 0:
                # 상
                is_po = False 
                for path in range(-1, self.dxy[direction][0], -1): 
                  if self.pieces[bef_x + (bef_y + path) * 9] != 0 or self.enemy_pieces[89 - (bef_x + (bef_y + path) * 9)] != 0: # 경로 중 뛰어 넘어 갈 기물이 있다면
                    if self.pieces[bef_x + (bef_y + path) * 9] != 4 and self.enemy_pieces[89 - (bef_x + (bef_y + path) * 9)] != 4: # 그 기물이 나 혹은 상대의 포가 아니라면
                      is_po = path + -1
                      break
                if is_po:
                  for path in range(is_po, self.dxy[direction][0]): # 기물을 뛰어 넘은 이후부터 경로를 다시 탐색 
                    if self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 0: # 상대편 보드에 기물이 있다면 행동추가 하고 break 
                      actions.append(self.position_to_action(p, direction))
                      break
                    elif self.pieces[(bef_x + path) + bef_y * 9] != 0: # 내 보드에 기물이 있다면 그냥 break
                      break
                    else:
                      actions.append(self.position_to_action(p, direction)) # 둘다 아닐 경우 행동추가
                # 하
                is_po = False 
                for path in range(-1, self.dxy[direction][0], -1):
                  if self.pieces[(bef_x + path) + bef_y * 9] != 0 or self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 0: # 경로 중 뛰어 넘어 갈 기물이 있다면
                    if self.pieces[(bef_x + path) + bef_y * 9] != 4 and self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 4: # 그 기물이 나 혹은 상대의 포가 아니라면
                      is_po = path - 1
                      break
                if is_po:
                  for path in range(is_po, self.dxy[direction][0], -1): # 기물을 뛰어 넘은 이후부터 경로를 다시 탐색 
                    if self.enemy_pieces[89 - ((bef_x + path) + bef_y * 9)] != 0: # 상대편 보드에 기물이 있다면 행동추가 하고 break 
                      actions.append(self.position_to_action(p, direction))
                      break
                    elif self.pieces[(bef_x + path) + bef_y * 9] != 0: # 내 보드에 기물이 있다면 그냥 break
                      break
                    else:
                      actions.append(self.position_to_action(p, direction)) # 둘다 아닐 경우 행동추가
            # 궁성안에 기물이 있을 때 대각선 행동 추가
            if self.dxy[direction][1] != 0 and self.dxy[direction][0] != 0:

                if position_src == 68: # 내 궁성에 있을 때
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]: # 궁성 가운데 포를 제외한 기물이 있다면
                    if (self.dxy[direction][1] == -2 and self.dxy[direction][0] == 2):
                      actions.append(self.position_to_action(p, direction))
                if position_src == 5: # 상대방 궁성에 있을 때
                  if self.pieces[13] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 13] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == -2 and self.dxy[direction][0] == 2):
                      actions.append(self.position_to_action(p, direction))

                if position_src == 86:
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == -2 and self.dxy[direction][0] == -2):
                      actions.append(self.position_to_action(p, direction))
                if position_src == 23:
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == -2 and self.dxy[direction][0] == -2):
                      actions.append(self.position_to_action(p, direction))


                if position_src == 84:
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == 2 and self.dxy[direction][0] == -2):
                      actions.append(self.position_to_action(p, direction))
                if position_src == 21:
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == 2 and self.dxy[direction][0] == -2):
                      actions.append(self.position_to_action(p, direction))


                if position_src == 66:
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == 2 and self.dxy[direction][0] == 2):
                      actions.append(self.position_to_action(p, direction))
                if position_src == 3:
                  if self.pieces[76] == [1, 2, 3, 5, 6, 7] and self.enemy_pieces[89 - 76] == [1, 2, 3, 5, 6, 7]:
                    if (self.dxy[direction][1] == 2 and self.dxy[direction][0] == 2):
                      actions.append(self.position_to_action(p, direction))
              
          # 사
          elif self.pieces[position_src] == 5:
            if 3 <= x and x <= 5 and 7 <= y and y <= 9: # 이동후의 위치가 궁성을 벗어나지 않는 다면
              actions.append(self.position_to_action(p, direction))
                
          # 상 
          elif self.pieces[position_src] == 6:
            if (bef_x + (bef_y - 1) * 9) <= 89:
              # 상우
              if self.pieces[bef_x + (bef_y - 1) * 9] and self.enemy_pieces[89 - (bef_x + (bef_y - 1) * 9)] == 0:
                if ((bef_x + 1) + (bef_y - 2) * 9) <= 89:
                  if self.pieces[(bef_x + 1) + (bef_y - 2) * 9] and self.enemy_pieces[89 - ((bef_x + 1) + (bef_y - 2) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

            if ((bef_x + 1) + bef_y * 9) <= 89:
              # 우상
              if self.pieces[(bef_x + 1) + bef_y * 9] and self.enemy_pieces[89 - ((bef_x + 1) + bef_y * 9)] == 0:
                if ((bef_x + 2) + (bef_y - 1) * 9) <= 89:
                  if self.pieces[(bef_x + 2) + (bef_y - 1) * 9] and self.enemy_pieces[89 - ((bef_x + 2) + (bef_y - 1) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

            if ((bef_x + 1) + bef_y * 9) <= 89:
              # 우하
              if self.pieces[(bef_x + 1) + bef_y * 9] and self.enemy_pieces[89 - ((bef_x + 1) + bef_y * 9)] == 0:
                if ((bef_x + 2) + (bef_y + 1) * 9) <= 89:
                  if self.pieces[(bef_x + 2) + (bef_y + 1) * 9] and self.enemy_pieces[89 - ((bef_x + 2) + (bef_y + 1) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

            if (bef_x + (bef_y + 1) * 9) <= 89:
              # 하우         
              if self.pieces[bef_x + (bef_y + 1) * 9] and self.enemy_pieces[89 - (bef_x + (bef_y + 1) * 9)] == 0:
                if ((bef_x + 1) + (bef_y + 2) * 9) <= 89:
                  if self.pieces[(bef_x + 1) + (bef_y + 2) * 9] and self.enemy_pieces[89 - ((bef_x + 1) + (bef_y + 2) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

            if (bef_x + (bef_y + 1) * 9) <= 89:
              # 하좌
              if self.pieces[bef_x + (bef_y + 1) * 9] and self.enemy_pieces[89 - (bef_x + (bef_y + 1) * 9)] == 0:
                if ((bef_x - 1) + (bef_y + 2) * 9) <= 89:
                  if self.pieces[(bef_x - 1) + (bef_y + 2) * 9] and self.enemy_pieces[89 - ((bef_x - 1) + (bef_y + 2) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))
            
            if ((bef_x - 1) + bef_y * 9) <= 89:
              # 좌하
              if self.pieces[(bef_x - 1) + bef_y * 9] and self.enemy_pieces[89 - ((bef_x - 1) + bef_y * 9)] == 0:
                if ((bef_x - 2) + (bef_y + 1) * 9) <= 89:
                  if self.pieces[(bef_x - 2) + (bef_y + 1) * 9] and self.enemy_pieces[89 - ((bef_x - 2) + (bef_y + 1) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

            if ((bef_x - 1) + bef_y * 9) <= 89:
              # 좌상
              if self.pieces[(bef_x - 1) + bef_y * 9] and self.enemy_pieces[89 - ((bef_x - 1) + bef_y * 9)] == 0:
                if ((bef_x - 2) + (bef_y - 1) * 9) <= 89:
                  if self.pieces[(bef_x - 2) + (bef_y - 1) * 9] and self.enemy_pieces[89 - ((bef_x - 2) + (bef_y - 1) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

            if (bef_x + (bef_y - 1) * 9) <= 89:
              # 상좌
              if self.pieces[bef_x + (bef_y - 1) * 9] and self.enemy_pieces[89 - (bef_x + (bef_y - 1) * 9)] == 0:
                if ((bef_x - 1) + (bef_y - 2) * 9) <= 89:
                  if self.pieces[(bef_x - 1) + (bef_y - 2) * 9] and self.enemy_pieces[89 - ((bef_x - 1) + (bef_y - 2) * 9)] == 0:
                    actions.append(self.position_to_action(p, direction))

          # 왕
          elif self.pieces[position_src] == 7:
            if 3 <= x and x <= 5 and 7 <= y and y <= 9: # 이동후의 위치가 궁성을 벗어나지 않는 다면
              actions.append(self.position_to_action(p, direction))
      return actions





      
state = State()
print(state.cal_piece_score())
print(state.cal_enemy_piece_score())
print(state.legal_actions())
print(len(state.legal_actions()))

for i in state.legal_actions():
  print('{} // 58 = {}'.format(i, i // 58))
  print('{} % 58 = {}'.format(i, i % 58))
  print('-----')