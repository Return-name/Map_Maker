import pygame, tkinter as tk
from pygame.locals import *
from tkinter import filedialog

MAPNAME = "green_map/main.map"
#MAPNAME = "temp.map"

class sprite:
    def __init__(self, surf, position, filename):
        self.surf = surf
        self.osurf = surf
        self.position = position
        self.rect = surf.get_rect()
        self.rect.topleft = position
        self.filename = filename
        self.type = 1           # 1-image
        self.angle = 0
        self.scale = 1.0
        self.collide = False
        self.oncollide = ""

    def rotate(self, angle):
        self.angle += angle
        t = self.rect.center
        self.surf = pygame.transform.rotozoom( self.osurf, self.angle, self.scale)
        self.rect = self.surf.get_rect()
        self.rect.center = t

    def changeSize(self, scale):
        self.scale *= scale
        t = self.rect.center
        self.surf = pygame.transform.rotozoom(self.osurf, self.angle, self.scale)
        self.rect = self.surf.get_rect()
        self.rect.center = t

class Static:
    def __init__(self, text, position):
        self.text = text
        self.surf = font.render(text, True, BLACK)
        self.rect = self.surf.get_rect()
        self.rect.topleft = position

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
        self.surf = font.render(self.text, True, BLACK)
        pos = self.rect.topleft
        self.rect = self.surf.get_rect()
        self.rect.topleft = pos

class Player:
    def __init__(self,screen_w,screen_h):
        self.img_list = []
        self.rect_list = []
        self.deltaframe = 7
        self.num = 0
        self.angle = 0
        self.screen_w = screen_w
        self.screen_h = screen_h

    def add_img(self, surf, rect):
        self.img_list.append(surf)
        self.rect_list.append(rect)

    def display(self, frame_num, angle):
        self.angle = angle
        if(frame_num % self.deltaframe == 0):
            self.num += 1
            if(self.num == len(self.img_list)):
                    self.num = 0
        r_img = pygame.transform.rotate(self.img_list[self.num],angle)
        r_rect = r_img.get_rect()
        r_rect.center = (self.screen_w//2,self.screen_h//2)
        return r_img, r_rect

    def display_idle(self):
        r_img = pygame.transform.rotate(self.img_list[0],angle)
        r_rect = r_img.get_rect()
        r_rect.center = (self.screen_w//2,self.screen_h//2)
        return r_img, r_rect

def update_oncollide(selected,t1,my_w):
    selected.oncollide = repr(t1.get("1.0",'end-1c'))
    my_w.destroy()

pygame.init()

pygame.display.set_caption("Map Maker")

screen_w = 1200
screen_h = 700
#screen_w, screen_h = 800,600
screen = pygame.display.set_mode((screen_w,screen_h))

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

background_color = WHITE

sprite_list = []
static_list = []
start_label_sprite = None

font = pygame.font.SysFont(None, 24)

edit_text1 ="EDITING MODE"
edit_text2 = "ESC: Quit      N: New_Sprite       P: Play_Mode        R: Rotate       L: Size     C: Collide_Toggle       U: Delete       F: Bring_Front       V: Duplicate"
edit_text_surf1 = font.render(edit_text1, True, BLACK)
edit_ts1_rect = edit_text_surf1.get_rect()
edit_text_surf2 = font.render(edit_text2, True, BLACK)
edit_ts2_rect = edit_text_surf2.get_rect()
edit_ts1_rect.center = (62, 665)
edit_ts2_rect.topleft = (5, 679)

play_text1 ="PLAYING MODE"
play_text2 = "P: Edit_Mode      W: Up       A: Left        S: Down       D: Right"
play_text_surf1 = font.render(play_text1, True, BLACK)
play_ts1_rect = play_text_surf1.get_rect()
play_text_surf2 = font.render(play_text2, True, BLACK)
play_ts2_rect = play_text_surf2.get_rect()
play_ts1_rect.topleft = (1, 660)
play_ts2_rect.topleft = (1, 680)

try:
    f = open(MAPNAME,'r')
    print("Map in " + MAPNAME + " opened successfully")
    l = f.read()
    l = l.split('\n')
    
    for pos,j in enumerate(l[:-1]):
        i = j.split(",",6)
        fn = i[0]
        if(fn[0] == "I"):
            surf = pygame.image.load(fn[2:])
            surf = surf.convert_alpha()
            ts = sprite(surf, [0,0] , fn[2:])
            ts.rotate(float(i[3]))
            ts.changeSize(float(i[4]))
            ts.rect.topleft = [int(i[1]),int(i[2])]
            if(str(i[5][2:]) == "True"):
                    ts.collide = True
            ts.oncollide = i[6]
            sprite_list.append(ts)
            if(pos == 0):
                start_label_sprite = ts
        elif (fn[0] == "T"):
            static_list.append(Static(fn[2:],(int(i[1]),int(i[2]))))
   
        print(fn, "opened")
    f.close()

except Exception as e:
    print(e)
    print("No Existing map found , loading the default one")
    surf = pygame.image.load("start_label.jpg").convert_alpha()
    ts = sprite(surf, [0,0], "start_label.jpg")
    ts.changeSize(0.350493899481)
    ts.rect.topleft = (500,300)
    ts.collide = False
    ts.oncollide = ""
    sprite_list.append(ts)
    start_label_sprite = ts
    print("Added start_label")

#setting the player
player = Player(screen_w,screen_h)
player_filenames = ["player_idle2.png","player_walk_front_right2.png","player_idle2.png","player_walk_front_left2.png"]
for i in player_filenames:
    t_img = pygame.image.load(i).convert()
    t_img.set_colorkey(t_img.get_at([5,5]))
    t_rect = t_img.get_rect()
    t_rect.center = screen_w//2,screen_h//2
    player.add_img(t_img, t_rect)

running = True

def save_map_disk(sprite_list, static_list):
    print("Saving Map to file "+ MAPNAME)
    f = open(MAPNAME,'w')
    for i in sprite_list:
        if(i.filename):
            if i.type == 1:
                f.write("I-")
            f.write(i.filename + "," + str(i.rect.topleft[0]) + "," + str(i.rect.topleft[1])+ "," + str(i.angle) + "," + str(i.scale) + "," + 'c=' + str(i.collide) + "," + i.oncollide + "\n")
    for j in static_list:
        f.write("T-" + j.getText() + "," + str(j.rect.topleft[0]) + "," + str(j.rect.topleft[1]) + "\n")
    f.close()


while running:
    moving = False
    angle = 0
    scale = 1

    selected_index = -1
    selected = 0
    editing = True
    moved = [0,0]
    clock = pygame.time.Clock()
    while editing:
        #print(selected)
        screen.fill(background_color)

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                running = False
                editing = False
                
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    editing = False

                elif event.key == K_n:
                    root = tk.Tk()
                    root.withdraw()
                    img_path = filedialog.askopenfilename()
                    root.destroy()
                    if(img_path):
                        img_sprite = pygame.image.load(img_path)
                        img_sprite = img_sprite.convert_alpha()
                        ts = sprite(img_sprite, [100-moved[0],100-moved[1]], img_path)
                        ts.collide = False
                        ts.oncollide = ""
                        sprite_list.append(ts)
                elif event.key == K_t:
                    print("Enter the text :-")
                    t = input()
                    st = Static(t, (200,200))
                    static_list.append(st)

                elif event.key == K_p:
                    editing = False
                elif event.key == K_d:
                    moved[0] -= 10
                elif event.key == K_a:
                    moved[0] += 10

            elif event.type == MOUSEMOTION: 
                if moving:
                   selected.rect.move_ip(event.rel)
                else:
                    """
                    if not (event.mod & KMOD_SHIFT):
                        for index,i in enumerate(sprite_list):
                            if(i.rect.move(moved).collidepoint(event.pos)):
                                selected = i
                                selected_index = index
                                break
                        else:
                            selected = 0
                            selected_index = -1
                    else:
                    """
                    if sprite_list[0].rect.move(moved).collidepoint(event.pos):
                        selected = sprite_list[0]
                        selected_index = 0
                    else:
                        for i in static_list:
                            if(i.rect.collidepoint(event.pos)):
                                #print("Collision with static object")
                                selected = i
                                selected_index = -1
                                break
                        else: 
                            for index,i in enumerate(sprite_list[::-1]):
                                if(i.rect.move(moved).collidepoint(event.pos)):
                                    selected = i
                                    selected_index = len(sprite_list) -1 - index
                                    break
                            else:
                                selected = 0
                                selected_index = -1
        
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    moved[1] += 20
                elif event.button == 5:
                    moved[1] -= 20
                elif event.button == 6:
                    moved[0] += 20
                elif event.button == 7:
                    moved[0] -= 20
            if selected:
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        if event.mod & KMOD_SHIFT:
                            selected.rotate(-10)
                        else:
                            selected.rotate(10)
                    elif event.key == K_l:
                        if event.mod & KMOD_SHIFT:
                            selected.changeSize(1/1.1)
                        else:
                            selected.changeSize(1.1)
                    elif event.key == K_c:
                        selected.collide = not selected.collide
                        if(selected.collide):
                            my_w = tk.Tk()
                            my_w.geometry("500x500")
                            t1 = tk.Text(my_w, height= 27, width= 60)
                            t1.grid(row=1, column = 1)
                            if selected.oncollide:
                                code = eval(selected.oncollide)
                            else:
                                code = "pass"
                            t1.insert(tk.END, code)
                            b1 = tk.Button(my_w, text="Done", width=10, bg="red", command=lambda: update_oncollide(selected,t1,my_w))
                            b1.grid(row=2,column=1)
                            my_w.mainloop()
                    elif event.key == K_v:
                        ts = sprite(selected.surf.copy(), selected.rect.topleft, selected.filename)
                        ts.angle = selected.angle
                        ts.scale = selected.scale
                        ts.collide = selected.collide
                        ts.oncollide = selected.oncollide
                        sprite_list.append(ts)
                    elif event.key == K_u:
                        sprite_list.pop(selected_index)
                    elif event.key == K_f:
                        sprite_list.pop(selected_index)
                        sprite_list.append(selected)
                        selected_index = len(sprite_list)-1
                elif event.type == MOUSEBUTTONDOWN:
                    moving = True
                elif event.type == MOUSEBUTTONUP:
                    moving = False
            
        for i in sprite_list:
            screen.blit(i.surf , i.rect.move(moved))
            if(i.collide == 1):
                pygame.draw.rect(screen, BLUE, i.rect.move(moved), 4)
            if(selected == i):
                pygame.draw.rect(screen, RED, i.rect.move(moved), 4)
        
        for i in static_list:
            screen.blit(i.surf, i.rect)

        screen.blit(start_label_sprite.surf , start_label_sprite.rect.move(moved))
        
        screen.blit(edit_text_surf1, edit_ts1_rect)
        screen.blit(edit_text_surf2, edit_ts2_rect)

        pygame.display.update()
        clock.tick(60)
    
    if(not running):
        #basically exit the application
        continue

    playing = True
    moved_dir = [False]*4
    start_rect = sprite_list[0].rect
    moved = [-start_rect.center[0]+600,-start_rect.center[1]+350]
    moved_old = moved.copy()

    frame_num = 1
    up_frame_num = 1
    clock = pygame.time.Clock()
    while playing:
        screen.fill(background_color)
    
        should_move = True
        for i in sprite_list:
            if(i.collide):
                if(i.rect.move(moved).colliderect(player.rect_list[0])):    #technically the 0 should be player.num
                    should_move = False
                    if i.oncollide:
                        exec(eval(i.oncollide))
                    break
        if(not should_move):
            moved = moved_old.copy()

        for i in sprite_list[1:]:
            screen.blit(i.surf, i.rect.move(moved))
        for i in static_list:
            screen.blit(i.surf, i.rect)
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    playing = False
                elif event.key == K_d:
                    moved_dir[0] = True
                elif event.key == K_a:
                    moved_dir[1] = True
                elif event.key == K_w:
                    moved_dir[2] = True
                elif event.key == K_s:
                    moved_dir[3] = True
            
            elif event.type == KEYUP:
                up_frame_num = 1
                if event.key == K_d:
                    moved_dir[0] = False
                elif event.key == K_a:
                    moved_dir[1] = False
                elif event.key == K_w:
                    moved_dir[2] = False
                    #up_frame_num = 1
                elif event.key == K_s:
                    moved_dir[3] = False
    
        moved_old = moved.copy()
       
        moving = False
        if(moved_dir[0]):
            moved[0] -= 5
            moving = True
            angle = -90
            up_frame_num += 1
        elif(moved_dir[1]):
            moved[0] += 5
            moving = True
            angle = 90
            up_frame_num += 1
        elif(moved_dir[2]):
            moved[1] += 5
            up_frame_num += 1
            moving = True
            angle  = 0 
        elif(moved_dir[3]):
            moved[1] -= 5
            moving = True
            up_frame_num += 1
            angle = 180
        
        if(moving):
            screen.blit(*player.display(up_frame_num, angle))
        
        if(not moving):
            screen.blit(*player.display_idle())
        
        screen.blit(play_text_surf1, play_ts1_rect)
        screen.blit(play_text_surf2, play_ts2_rect)

        pygame.display.update()
        frame_num += 1
        if(frame_num == 61):
            frame_num = 1
        clock.tick(60)

pygame.quit()
while(True):
    i = input("Save to disk? y/n : ")
    if i == 'y' or i == "Y" or i == "yes" or i == "Yes":
        save_map_disk(sprite_list, static_list)
        break
    elif i == 'n' or i == "N" or i == "no" or i == "No":
        break
    else:
        print("Sorry, Enter again ")


#print("Save Completed")

