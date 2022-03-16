# Author: aqeelanwar
# Created: 12 June,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

# Icons: https://www.flaticon.com/authors/freepik
from tkinter import *
import random
import time
import numpy as np
from PIL import ImageTk,Image
import math
import nltk
random.seed(random.random())
# Define useful parameters
red_kitchen = "#F2003C"
cyan_livingroom = "#00B7EB"
orange_bedroom = "#FF7F00"
purple_studio = "#B600F2"
aoi_bathroom = "#232B6C"
yellow_balcony="#FFFF00"
bound = "#4B9687"
size_of_board = 600
rows = 40
cols = 40
DELAY = 10
snake_initial_length = 1
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 2
RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"
Black_color = "#050504"
BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'
#wall =[(0,0),(0,1),(0,2)]
#occupied_wall = []
Areas = {"a1":[0,0,39,3] , "a2":[0,4,1,23], "a3":[0,24,7,39],
"a4":[8,35,33,39],"a5":[34,36,39,39],"a6":[25,4,39,6] , 
"a7":[38,7,39,35],"a8":[2,9,4,9],"a9":[7,9,15,9],
"a10":[14,10,14,19],"a11":[15,19,18,19],"a12":[18,9,26,9],
"a13":[26,7,26,8],"a14":[36,7,37,9],"a15":[37,35,37,35],
"a16":[19,25,19,34],"a17":[18,24,21,24],"a18":[8,30,14,30],
"a19":[14,24,14,26],"a20":[8,26,14,26],"a21":[24,10,24,18],
"a22":[22,19,24,19]     }

obstacle=[]

Furniture={"f1":[2,10,3,22],"f2":[4,12,9,18],"f3":[4,20,4,21],
"f4":[8,24,13,25],"f5":[8,28,10,29],"f6":[14,33,16,34],
"f7":[17,31,18,34],"f8":[18,25,18,30],"f9":[20,25,21,33],
"f10":[22,33,33,34],"f11":[25,25,31,27],"f12":[37,10,37,28],
"f13":[34,11,36,19],"f14":[31,15,32,16],"f15":[27,7,35,9],
"f16":[25,10,26,19],"f17":[22,10,23,13],"f18":[23,14,23,18],
"f19":[25,7,25,8],"f20":[23,4,24,8]}

object={"b1":[2,4,3,5],"b2":[3,21,3,21],"b3":[10,24,11,24],
"b4":[18,28,18,29],"b5":[20,34,21,34],"b6":[26,33,28,33],
"b7":[26,24,27,24],"b8":[29,24,30,24],"b9":[26,28,27,28],
"b10":[29,28,30,28],"b11":[32,20,32,20],"b12":[31,13,31,13],
"b13":[31,16,31,16],"b14":[36,10,36,10],"b21":[26,26,26,26],
"b15":[27,10,28,11],"b16":[23,6,23,6],"b17":[23,8,23,8],
"b18":[21,11,21,12],"b19":[23,11,23,11],"b20":[23,13,23,13]}


walkable = [(x,y) for x in range(0,40) for y in range(0,40)]

walk_ranking={}

visited =[]

walls=[]


boundary_point={"balcony_bedroom":[],"balcony_studio":[],"bedroom_bathroom":[], 
"bedroom_kitchen":[],"kitchen_studio":[], "livingroom_kitchen":[]}

knowledge_belong ={"balcony_plants":["balcony"],
"living_plants":["livingroom"],
"sunglass":["bedroom"],"clothes":["bedroom"],
"toothbrush":["bathroom"],
 "apple":["kitchen"],
"light":["livingroom"],"computer":["studio"],
"bowl":["kitchen"],"kitchen_chair":["kitchen"],
"studio_chair":["studio"],
"living_chair":["livingroom"],
"phone":["studio"],"bread":["kitchen"],
"snacks":["livingroom"],
"tv":["livingroom"],
"toilet":["bathroom"],
"washstand":["bathroom"],
"night_table":["bedroom"],
"sofa":["livingroom"],
"bay_window":["livingroom"],
"tea_table":["livingroom"],
"kitchen_table":["kitchen"],
"studio_table":["studio"],
"cooking_bench":["kitchen"],
"cabinet":["livingroom"],
"bed":["bedroom"],
"bath_cabinet":["bathroom"]}
ground_truth = {"balcony_plants":[(2,4),(2,5),(3,4),(3,5),(23,6),(23,8)],
"living_plants":[(27,10),(27,11),(28,10),(28,11)],
"sunglass":[(3,21)],"clothes":[(10,24),(11,24)],
"toothbrush":[(18,28),(18,29)],"bread":[(20,34),(21,34)],"apple":[(26,33),(28,33)],
"living_chair":[(31,13)],
"studio_chair":[(21,11),(21,12)],
"kitchen_chair":[(26,24),(27,24),(29,24),(30,24),(26,28),(27,28),(29,28),(30,28),(32,20)],"bowl":[(26,26)],
"snacks":[(31,16)],"light":[(36,10)],"phone":[(23,13)],"computer":[(23,11)],
"cooking_bench":[(18,33)],"studio_table":[(21,12)],"kitchen_table":[(26,26)],
"sofa":[(34,16)],"cabinet":[(24,6)],"tea_table":[(32,16)],"bay_window":[(29,8)],"tv":[(23,15)],
"bed":[(5,15)],"night_table":[(3,11),(3,20)],"washstand":[(18,26)],"toilet":[(8,28)],"bath_cabinet":[(14,34)]}

furni_points=[(18,33),(21,12),(26,26),(34,16),(24,6),(32,16),(29,8),(23,15),(5,15),(3,11),(3,20),(18,26),(14,34),(8,28)]


section =["bedroom","livingroom","kitchen","balcony","studio","bathroom"]

class SnakeAndApple:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)
        self.window.bind("<Button-1>", self.mouse_input)
        self.play_again()
        self.begin = False
        self.memory ={}
            
    def wall_printer(self,x1,y1,x2,y2):

        for area in Areas.values():
           x1 = area[0]
           x2 = area[2]
           y1 = area[1]
           y2 = area[3]
           coordinates = [(x,y) for x in range(x1,x2+1) for y in range(y1,y2+1)]
           #print(coordinates)
           for tuple in coordinates:
               self.place_apple(tuple[0],tuple[1])
               obstacle.append((tuple[0],tuple[1]))
               walls.append((tuple[0],tuple[1]))

    def furn_printer(self,x1,y1,x2,y2):
        for furn in Furniture.values():
           x1 = furn[0]
           x2 = furn[2]
           y1 = furn[1]
           y2 = furn[3]
           coordinates = [(x,y) for x in range(x1,x2+1) for y in range(y1,y2+1)]
         
           for tuple in coordinates:
               self.place_furniture(tuple[0],tuple[1])
               obstacle.append((tuple[0],tuple[1]))

    def obj_printer(self,x1,y1,x2,y2):
        for obj in object.values():
           x1 = obj[0]
           x2 = obj[2]
           y1 = obj[1]
           y2 = obj[3]
           coordinates = [(x,y) for x in range(x1,x2+1) for y in range(y1,y2+1)]

           for tuple in coordinates:
               self.place_object(tuple[0],tuple[1])
               obstacle.append((tuple[0],tuple[1]))

    def sec_printer(self):
        allpoints = [(x,y) for x in range(40) for y in range(40)]
               
        for x in obstacle:
           
           if x in allpoints:
              allpoints.remove(x)
        for e in allpoints:
            sec = self.predict_section(e[0],e[1])
            #print("sssss"+str(e))
            if sec=="livingroom":
                  self.place_livingroom(e[0],e[1])
            elif sec == "kitchen":
                  self.place_kitchen(e[0],e[1])
            elif sec=="studio":
                  self.place_studio(e[0],e[1])
            elif sec=="balcony":
                  self.place_balcony(e[0],e[1])
            elif sec=="bathroom":
                  self.place_bathroom(e[0],e[1])
            elif sec=="bedroom":
                  self.place_bedroom(e[0],e[1])
            else:
                 print("immmmmmmmmmmsssss")

   

    def initialize_board(self):
        self.board = []
        self.apple_obj = []
        self.old_apple_cell = []

        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))

        for i in range(rows):
            self.canvas.create_line(
                i * size_of_board / rows, 0, i * size_of_board / rows, size_of_board,
            )

        for i in range(cols):
            self.canvas.create_line(
                0, i * size_of_board / cols, size_of_board, i * size_of_board / cols,
            )

    def initialize_snake(self):
       
        self.snake = []
        self.crashed = False
        self.snake_heading = "Right"
        self.last_key = self.snake_heading
        self.forbidden_actions = {}
        self.forbidden_actions["Right"] = "Left"
        self.forbidden_actions["Left"] = "Right"
        self.forbidden_actions["Up"] = "Down"
        self.forbidden_actions["Down"] = "Up"
        self.snake_objects = []
        for i in range(snake_initial_length):
            self.snake.append((i+35,35))

    def play_again(self):
        #playagain
        self.canvas.delete("all")
        self.initialize_board()
        self.initialize_snake()
        
        self.place_balcony(22,6)        
        self.wall_printer(0,0,39,3)
        self.furn_printer(0,0,0,0)
        self.obj_printer(25,25,1,1)
        #print(obstacle)
        #print("************************8")
        self.sec_printer()   
        for x in obstacle:
           if x in walkable:
               walkable.remove(x)


          
         



        for e in walkable:
            walk_ranking[e]=0
      #      self.boundarypoint(e[0],e[1])
           # self.place_bound(e[0],e[1])
      #      print(boundary_point)
      #      print("*****************")
        self.display_snake(mode="complete")
        self.begin_time = time.time()

    def get_key(self,val,dict):
        for key, value in dict.items():
            if val == value:
                return key
 
        return "key doesn't exist"


    def wall_block(self,loc1,loc2,x1,y1):

        x_min = min(loc1,x1)
        x_max = max(loc1,x1)
        y_min = min(loc2,y1)
        y_max = max(loc2,y1)
        count = 0         
        list = []
        for  e in range(x_min,x_max+1):
            list.append((e,y_min))
            list.append((e,y_max))
          
 
        for  e in range(y_min,y_max+1):
            list.append((x_min,e))
            list.append((x_max,e))
        
        for e in list:
            if e in  walls:
                count+=1

        return count*10000

        
        



    def predict_section(self,x1,y1):
        #print(obstacle)
        if (x1,y1) in obstacle:
            return "obstacles"
        vote_dict ={}
        for e in section:
            vote_dict[e]=0

        list_values =[]
        factor = 100
        for obje in ground_truth.keys():
            for location in ground_truth[obje]:
                eud_dis=(location[0]-x1)**2+(location[1]-y1)**2
               # print(x1)
               # print(y1)
                for sec in knowledge_belong[obje]:
                   temp = factor/(eud_dis)
                   temp /= (self.wall_block(location[0],location[1],x1,y1)+1)
                   vote_dict[sec] += temp
        #print(vote_dict)              
        value_list = list(vote_dict.values())
        value_list.sort(reverse=True)
       # print("predict section")
        pre_sec = self.get_key(value_list[0],vote_dict)
       # print(pre_sec)
        return pre_sec       
   


#    def wall_barrier(self):
           

    def movement(self):

        move=["Up","Left","Right","Down"]
        down_pos = (self.snake[0][0], self.snake[0][1]+1)
        up_pos = (self.snake[0][0], self.snake[0][1]-1)
        left_pos = (self.snake[0][0]-1, self.snake[0][1])
        right_pos = (self.snake[0][0]+1, self.snake[0][1])
        nex_pos =[down_pos, up_pos, left_pos, right_pos]

        temp_dict={}

        if down_pos in obstacle:
              move.remove("Down")
              nex_pos.remove(down_pos)
        if up_pos in obstacle:
              move.remove("Up")
              nex_pos.remove(up_pos)
        if left_pos in obstacle:
              move.remove("Left")
              nex_pos.remove(left_pos)
        if right_pos in obstacle:
              move.remove("Right")
              nex_pos.remove(right_pos)
        for e in nex_pos:

            temp_dict[e]=walk_ranking[e] 
        
        
        least_visit = min(temp_dict.values())
        pose = []
        for k,v in temp_dict.items():
            if v == least_visit:
               pose.append(k)
                
        least_pos = random.choice(pose) 
        #least_pos = self.get_key(least_visit,temp_dict)
                
        if down_pos == least_pos:
            next_move = "Down"
        elif up_pos == least_pos:
            next_move = "Up"
        elif left_pos == least_pos:
            next_move = "Left"
        else:
            next_move = "Right"
        return  next_move      
    
    def e_distance(self,x1,y1,x2,y2):
       # print(x1,y1,x2,y2)
        if ((x2-x1)**2+(y2-y1)**2)< 10:
            return 1
        return 0 


    def boundarypoint(self,x,y):
        flag = 0
        four_direct = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        for e in four_direct:
            if self.predict_section(e[0],e[1])== "balcony" and self.predict_section(x,y)=="bedroom":
               boundary_point["balcony_bedroom"].append((x,y))
               self.place_bound(x,y)
            if self.predict_section(e[0],e[1])== "balcony" and self.predict_section(x,y)=="studio":
               boundary_point["balcony_studio"].append((x,y))
               self.place_bound(x,y)
            if self.predict_section(e[0],e[1])== "bedroom" and self.predict_section(x,y)=="bathroom":
               boundary_point["bedroom_bathroom"].append((x,y))
               self.place_bound(x,y)
            if self.predict_section(e[0],e[1])== "bedroom" and self.predict_section(x,y)=="kitchen":
               boundary_point["bedroom_kitchen"].append((x,y))
               self.place_bound(x,y)
            if self.predict_section(e[0],e[1])== "kitchen" and self.predict_section(x,y)=="studio":
               boundary_point["kitchen_studio"].append((x,y))
               self.place_bound(x,y)
            if self.predict_section(e[0],e[1])=="livingroom" and self.predict_section(x,y) =="kitchen":
               boundary_point["livingroom_kitchen"].append((x,y))
               self.place_bound(x,y)
              
     
    def navigate(self,loc1,loc2):
        horiz_move = "h"
        verti_move = "v"
        case = 10
        if loc1>=self.snake[0][0] and loc2 >= self.snake[0][1]:
           case = 1
        elif loc1>=self.snake[0][0] and loc2 <= self.snake[0][1]:
           case = 2
        elif loc1<=self.snake[0][0] and loc2 >= self.snake[0][1]:
           case = 3
        elif loc1<=self.snake[0][0] and loc2 <= self.snake[0][1]:
           case = 4
        else:
           case = 10

               
        while (self.snake[0][0]!= loc1 ):
             if case ==1 or case ==2:
                horiz_move = "Right"
                if (self.snake[0][0]+1,self.snake[0][1]) in obstacle:
                     
                      self.window.after(DELAY,self.update_snake("Down" if case ==1 else "Up"))    
             else:
                horiz_move = "Left"
                if (self.snake[0][0]-1,self.snake[0][1]) in obstacle:
                      
                      self.window.after(DELAY,self.update_snake("Down" if case ==3 else "Up"))

             self.window.after(DELAY,self.update_snake(horiz_move))
                
       
        while (self.snake[0][1]!= loc2 ):
             if case ==1 or case ==3:
                verti_move = "Down"
                if (self.snake[0][0],self.snake[0][1]+1) in obstacle:

                      self.window.after(DELAY,self.update_snake("Right" if case ==1 else "Left"))

             else:
                verti_move = "Up"
                if (self.snake[0][0],self.snake[0][1]-1) in obstacle:

                      self.window.after(DELAY,self.update_snake("Right" if case ==2 else "Left"))

             self.window.after(DELAY,self.update_snake(verti_move))
        
        return 0
        

#    def agent_navigate(self,x,y,a,b):
        
        
    def hit_wall(self,gx,gy,ix,iy):
        
        small_x = min(gx,ix)
        small_y = min(gy,iy)        
        big_x = max(gx,ix)
        big_y = max(gy,iy)
        l = [(x,y) for x in range(small_x,big_x) for y in range(small_y,big_y)]
        



    def observe(self):
        for e in ground_truth.values():
            for sub_e in e:
                 if self.e_distance(self.snake[0][0],self.snake[0][1],sub_e[0],sub_e[1]) == 1:
                    item_name = self.get_key(e,ground_truth)
                    if item_name not in self.memory.keys():
                        self.memory[item_name]=[sub_e]
                    elif sub_e not in self.memory[item_name]:
                        self.memory[self.get_key(e,ground_truth)].append(sub_e) 
                   # print("object"+self.get_key(e,ground_truth)+" observe")
                   # print(self.memory)
    def explore_covered(self):
        cont = sum(x == 0 for x in walk_ranking.values())
        print("percent")
        print(cont)
        print(len(walk_ranking.values()))

    def mainloop(self):
        index = 0 

        while True:
            #index +=1
            if (index == 500):
                  self.explore_covered()
                  print(self.memory)
                 # self.sec_printer()
                 # print("lolll")
                  break              
            self.window.update()
            
            if self.begin:
                 index +=1
                
                 walk_ranking[(self.snake[0][0],self.snake[0][1])]+=1
                # self.boundarypoint(self.snake[0][0],self.snake[0][1])
                 self.observe()
                 self.last_key =self.movement()
                 #self.place_balcony(self.snake[0][0],self.snake[0][1])
                 #if (index == 600):
                                
                     #self.navigate(35,35)
                  #   print("agent is back to original point!!!")
                  #   break
                 #print("step:"+str(index)) 
                 self.window.after(DELAY,self.update_snake(self.last_key))
                 #print(boundary_point)
       # print(walk_ranking) 
           #     if not self.crashed:
            #        self.window.after(DELAY, self.update_snake(self.last_key))
            #    else:
            #        self.begin = False
            #        self.display_gameover()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def display_gameover(self):
        score = len(self.snake)
        self.canvas.delete("all")
        score_text = "Scores \n"

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10

        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 8,
            font="cmr 40 bold",
            fill=Green_color,
            text=score_text,
        )
        score_text = str(score)
        self.canvas.create_text(
            size_of_board / 2,
            1 * size_of_board / 2,
            font="cmr 50 bold",
            fill=BLUE_COLOR,
            text=score_text,
        )
        time_spent = str(np.round(time.time() - self.begin_time, 1)) + 'sec'
        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 4,
            font="cmr 20 bold",
            fill=BLUE_COLOR,
            text=time_spent,
        )
        score_text = "Click to play again \n"
        self.canvas.create_text(
            size_of_board / 2,
            15 * size_of_board / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def place_apple(self,m1,m2):
        # Place apple randomly anywhere except at the cells occupied by snake
        #unoccupied_cels = set(self.board) - set(self.snake)
        #unoccupied_cels = set(wall)-set(occupied_wall)
        self.apple_cell = (m1,m2)
        #self.apple_cell = random.choice(list(unoccupied_cels))
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=Black_color, outline=BLUE_COLOR,
        )
        return self.apple_cell


    def place_furniture(self,x,y):
        #unoccupied_cels = set(self.board) - set(self.snake)
        #self.apple_cell = random.choice(list(unoccupied_cels))
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=RED_COLOR_LIGHT, outline=BLUE_COLOR,
        )
        return x,y
    
    def place_kitchen(self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=red_kitchen, outline=BLUE_COLOR,
        )
        return x,y 
 
    def place_studio(self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=purple_studio, outline=BLUE_COLOR,
        )
        return x,y

    def place_livingroom(self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=cyan_livingroom, outline=BLUE_COLOR,
        )
        return x,y

    def place_bound(self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=bound, outline=BLUE_COLOR,
        )
        return x,y

    def place_bedroom (self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=orange_bedroom, outline=BLUE_COLOR,
        )
        return x,y


    def place_balcony(self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=yellow_balcony, outline=BLUE_COLOR,
        )
        return x,y

    def place_bathroom(self,x,y):
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=aoi_bathroom, outline=BLUE_COLOR,
        )
        return x,y





    def place_object(self,x,y):
        #unoccupied_cels = set(self.board) - set(self.snake)
        #self.apple_cell = random.choice(list(unoccupied_cels))
        self.apple_cell =(x,y)
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=Green_color, outline=BLUE_COLOR,
        )


    def display_snake(self, mode=""):
        # Remove tail from display if it exists
        if self.snake_objects != []:
            self.canvas.delete(self.snake_objects.pop(0))
        if mode == "complete":
            for i, cell in enumerate(self.snake):
                # print(cell)
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = cell[0] * row_h
                y1 = cell[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=BLUE_COLOR,
                    )
                )
        else:
            # only update head
            cell = self.snake[-1]
            row_h = int(size_of_board / rows)
            col_w = int(size_of_board / cols)
            x1 = cell[0] * row_h
            y1 = cell[1] * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.snake_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR,
                )
            )
            if self.snake[0] == self.old_apple_cell:
                self.snake.insert(0, self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = tail[0] * row_h
                y1 = tail[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.insert(
                    0,
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR
                    ),
                )
            self.window.update()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def update_snake(self, key):
        # Check if it hit the wall or its own body

        tail = self.snake[0]
        head = self.snake[-1]
        if tail != self.old_apple_cell:
            self.snake.pop(0)
        if key == "Left":
            self.snake.append((head[0] - 1, head[1]))
        elif key == "Right":
            self.snake.append((head[0] + 1, head[1]))
        elif key == "Up":
            self.snake.append((head[0], head[1] - 1))
        elif key == "Down":
            self.snake.append((head[0], head[1] + 1))

        head = self.snake[-1]
#extra 2 lines
        self.snake_heading = key
        self.display_snake()
        #if (
       #         head[0] > cols - 1
       #         or head[0] < 0
       #         or head[1] > rows - 1
       #         or head[1] < 0
       #         or len(set(self.snake)) != len(self.snake)
       # ):
            # Hit the wall / Hit on body
      #      self.crashed = False
      #  elif (self.apple_cell == head) and 1==2:
            # Got the apple
      #      self.old_apple_cell = self.apple_cell
      #      self.canvas.delete(self.apple_obj)
      #      self.place_apple()
      #      self.display_snake()
      #  else:
      #      self.snake_heading = key
      #      self.display_snake()
    def up_snake(self,key):
        return
    def check_if_key_valid(self, key):
        valid_keys = ["Up", "Down", "Left", "Right"]
        if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
            return True
        else:
            return False

    def mouse_input(self, event):
        self.play_again()

    def key_input(self, event):
        if not self.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.check_if_key_valid(key_pressed):
                # print(key_pressed)
                self.begin = True
                self.last_key = key_pressed


game_instance = SnakeAndApple()
game_instance.mainloop()
