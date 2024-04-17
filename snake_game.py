import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
#Point = namedtuple('Point', 'x, y')

class Point:

    def __init__(self, x, y):
        self.x= x
        self.y= y
        self.coordinates= (x, y)


# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (10, 255, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:
    
    def __init__(self, w=640, h=640):
        self.gameIteration= 0
        self.gameFrame= 0
        self.w = w
        self.h = h
        self.reward= 0
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
       

    def reset(self):
        self.direction = Direction.RIGHT
        STARTING_POSITION= Point(self.w/2, self.h/2)
        self.head = STARTING_POSITION
        self.snake = [self.head.coordinates, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y).coordinates,
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y).coordinates]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.gameIteration +=1
        self.gameIteration= 0
        self.reward= 0
        
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step_ai(self, action):

        self.gameFrame+=1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
          
        
        # 2. move
        self._move_ai(action) # update the head
        self.snake.insert(0, self.head.coordinates)
        
        # 3. check if game over
        game_over = False
        if self._is_collision() or self.gameFrame > 100*len(self.snake):
            game_over = True
            self.reward= -10
            return self.reward, game_over, self.score
 
            
        # 4. place new food or just move
        if self.head.coordinates == self.food.coordinates:
            self.score += 1
            self.reward= 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return self.reward, game_over, self.score
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head.coordinates)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head.coordinates == self.food.coordinates:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision_ai(self, pt= None):
        if pt is None:
            pt= self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt.coordinates in self.snake[1:]:
            return True
        
        return False
   
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head.coordinates in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
         
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt[0]+4, pt[1]+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move_ai(self, action):
            #[left, straight, right]
            clock_wise= [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
            idx= clock_wise.index(self.direction)


            if action[0] == 1:
                #print("go left")
                new_direction= clock_wise[(idx-1)%4]  

            elif action[1] == 1:
               # print("go straight")
                new_direction= clock_wise[idx]

            else:
               # print("go right")
                new_direction= clock_wise[(idx+1)%4] 

            self.direction= new_direction 

            x = self.head.x
            y = self.head.y
            if self.direction == Direction.RIGHT:
                x += BLOCK_SIZE
            elif self.direction == Direction.LEFT:
                x -= BLOCK_SIZE
            elif self.direction == Direction.DOWN:
                y += BLOCK_SIZE
            elif self.direction == Direction.UP:
                y -= BLOCK_SIZE
            
            self.head = Point(x, y)
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)



class SnakeGameAI:
    
    def __init__(self, w=640, h=640):
        self.gameIteration= 0
        self.gameFrame= 0
        self.w = w
        self.h = h
        self.reward= 0
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
       

    def reset(self):
        self.direction = Direction.RIGHT
        STARTING_POSITION= Point(self.w/2, self.h/2)
        self.head = STARTING_POSITION
        self.snake = [self.head.coordinates, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y).coordinates,
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y).coordinates]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.gameIteration +=1
        self.gameIteration= 0
        self.reward= 0
        
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step_ai(self, action):

        self.gameFrame+=1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
          
        
        # 2. move
        self._move_ai(action) # update the head
        self.snake.insert(0, self.head.coordinates)
        
        # 3. check if game over
        game_over = False
        if self.is_collision() or self.gameFrame > 100*len(self.snake):
            game_over = True
            self.reward= -10
            return self.reward, game_over, self.score, self.gameIteration
 
            
        # 4. place new food or just move
        if self.head.coordinates == self.food.coordinates:
            self.score += 1
            self.reward= 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return self.reward, game_over, self.score, self.gameIteration
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head.coordinates)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head.coordinates == self.food.coordinates:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def is_collision_ai(self, pt= None):
        if pt is None:
            pt= self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt.coordinates in self.snake[1:]:
            return True
        
        return False
   
    def is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head.coordinates in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
      
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))
           # pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt[0]+4, pt[1]+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move_ai(self, action):
            #[left, straight, right]
            clock_wise= [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
            idx= clock_wise.index(self.direction)


            if action[0] == 1:
                #print("go left")
                new_direction= clock_wise[(idx-1)%4]  

            elif action[1] == 1:
                #print("go straight")
                new_direction= clock_wise[idx]

            else:
                #print("go right")
                new_direction= clock_wise[(idx+1)%4] 

            self.direction= new_direction 

            x = self.head.x
            y = self.head.y
            if self.direction == Direction.RIGHT:
                x += BLOCK_SIZE
            elif self.direction == Direction.LEFT:
                x -= BLOCK_SIZE
            elif self.direction == Direction.DOWN:
                y += BLOCK_SIZE
            elif self.direction == Direction.UP:
                y -= BLOCK_SIZE
            
            self.head = Point(x, y)
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGameAI()
    #game = SnakeGame()
    left= [1,0,0]
    straight= [0,1,0]
    right= [0,0,1]
    n= 0
    # game loop
    while True:
        reward, game_over, score, gameIteration = game.play_step_ai(straight)
        #game_over, score = game.play_step()
        #print(reward, gameIteration)

        if game_over ==True:
            game.reset()
            n+=1
        print("try number: ", n)
        print("reward: ", reward)

        
      
        
    print('Final Score', score)
        
        
    pygame.quit()