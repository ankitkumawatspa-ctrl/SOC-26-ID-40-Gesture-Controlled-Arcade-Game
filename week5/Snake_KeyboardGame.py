import pygame
import sys
import random
cell_size = 30
grid_W= 30
grid_H= 22

width= cell_size* grid_W
height= cell_size* grid_H

#Now specifying colors 

BG_color= (45,45,80)
S_head= (0,245,150)
S_body= (0,150,90)
Food_color= (240,70,60)
text_color = (235, 235, 245)
grid_color= (30,30,50)


# now defining functions

def random_food_pos(snake):
    while True:
        pos= (random.randint(2,grid_W-3),random.randint(2,grid_H-3))
        if pos not in snake:
            return pos



def draw_cell(surface, pos ,color):
    x= pos[0]*cell_size
    y= pos[1]*cell_size
    rect= pygame.Rect(x,y,cell_size,cell_size)
    pygame.draw.rect(surface,color,rect)
    pygame.draw.rect(surface, BG_color, rect, 1)




#main loop
def main():
    pygame.init()
    screen= pygame.display.set_mode((width,height))
    pygame.display.set_caption("SNAKE GAME")
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)





    #game initial point
    def reset_game():
        start= (grid_W//2 , grid_H//2)
        return [start], (1,0), random_food_pos([start]),0
    
    snake, direction , food, score = reset_game()



    #in the starting the boolean form of given below are
    g_over =False
    g_pause = False
    g_start = False
    score =0
    high_score=0


    #Game Speed Control
    delay_start = 200
    delay_min= 80
    delay_current= delay_start
    speed_step= 5
    last_move_time= pygame.time.get_ticks()     #returns the number of milliseconds (1/1000 of a second) that have passed since Pygame



    while True:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit() 
                if not g_start:
                    if event.key == pygame.K_SPACE:
                        g_start=True
                        snake , direction , food, score = reset_game()
                        last_move_time = pygame.time.get_ticks()
                        delay_current= delay_start

                elif g_over:
                    if event.key == pygame.K_SPACE:
                        snake , direction , food, score = reset_game()
                        g_over= False
                        g_pause = False
                        last_move_time = pygame.time.get_ticks()
                        delay_current= delay_start
                
                else:
                    if event.key == pygame.K_p:
                        g_pause= not g_pause

                    #game controls
                    if not g_pause:
                            if event.key == pygame.K_UP and direction != (0, 1):         
                                direction = (0, -1)
                            elif event.key == pygame.K_DOWN and direction != (0, -1):      
                                direction = (0, 1)
                            elif event.key == pygame.K_LEFT and direction != (1, 0):       
                                direction = (-1, 0)
                            elif event.key == pygame.K_RIGHT and direction != (-1, 0):     
                                direction = (1, 0)
            

#UPDATE

        c_time= pygame.time.get_ticks()



        if g_start and not g_pause and not g_over and ( c_time - last_move_time >=delay_current):
            last_move_time = c_time
            head = snake[0]
            new_head= (head[0]+direction[0],head[1]+direction[1])
            hit_wall= (new_head[0]<0 or new_head[0]>=grid_W or new_head[1]<0 or new_head[1]>= grid_H)
            hit_self = new_head in snake
            print(new_head[0]+direction[0])

            if hit_wall or hit_self:        
                g_over = True
                if score > high_score:      
                    high_score = score
            
            else:
                snake.insert(0,new_head)  #adding the snake pos at  zero index

                if new_head==food:
                    score+=1
                    food= random_food_pos(snake)
                    delay_current=max(delay_min, delay_current-speed_step)
                else:
                    snake.pop()  #removes the element of last index 
        
        #Rendering
        screen.fill(BG_color)
        if not g_start:
            title_surf = big_font.render("SNAKE GAME", True, S_head)
            sub_surf   = font.render("Press SPACE to start", True, text_color)
            screen.blit(title_surf, (width//2 - title_surf.get_width()//2, height//2 - 40))
            screen.blit(sub_surf,   (width//2 - sub_surf.get_width()//2,   height//2 + 20))

        else:
            for gx in range(grid_W):   
                pygame.draw.line(screen,grid_color, (gx*cell_size, 0), (gx*cell_size, height))   #vertical line
            for gy in range(grid_H):
                pygame.draw.line(screen, grid_color, (0, gy*cell_size), (width, gy*cell_size))   #horizontal line
            
            draw_cell(screen, food, Food_color)
            for i, segment in enumerate(snake):     # enumerate gives both the index i and the segment position
                color = S_head if i==0 else S_body
                draw_cell(screen, segment, color)
            

            score_surf = font.render(f"Score: {score}", True, text_color)
            hs_surf    = font.render(f"Best: {high_score}", True, (255, 215, 0))
            screen.blit(score_surf, (8, 6))
            screen.blit(hs_surf, (width - hs_surf.get_width() - 8, 6))
            

            if g_pause and not g_over:
                pause_surf = big_font.render("PAUSED", True, text_color)
                sub_surf   = font.render("Press P to resume", True, text_color)
                screen.blit(pause_surf, (width//2 - pause_surf.get_width()//2, height//2 - 40))
                screen.blit(sub_surf,   (width//2 - sub_surf.get_width()//2,   height//2 + 15)) 
            if g_over:
                msg = big_font.render("GAME OVER", True, Food_color)
                sub = font.render("Press SPACE to restart   |   Q to quit", True, text_color)
                screen.blit(msg, (width//2 - msg.get_width()//2, height//2 - 40))
                screen.blit(sub, (width//2 - sub.get_width()//2, height//2 + 15))

        pygame.display.flip()
if __name__ == "__main__":          # __name__ is a special Python variable. When you run this file directly (python3 snake_game_keyboard.py), Python sets __name__ to "__main__", so main() is called. 
    main()






















    

