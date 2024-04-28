import pygame
import random
from utils import Direction, Point, Colors

BLOCK_SIZE = 20
WIDTH = BLOCK_SIZE * 32
HEIGHT = BLOCK_SIZE * 32
SPEED = 40


class SnakeGameAI:
    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h
        self.gameInit = pygame.init()
        self.font = pygame.font.SysFont('arial', 25)
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.reset()

    def reset(self):
        self.gameOver = False
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head.coordinates,
            Point(self.head.x - BLOCK_SIZE, self.head.y).coordinates,
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y).coordinates
        ]

        self.score = 0
        self.apple = None
        self._place_apple()
        self.gameFrame = 0

    def _place_apple(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.apple = Point(x, y)
        if self.apple in self.snake:
            self._place_apple()

    def play_step_ai(self, action):
        self.gameFrame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._move_ai(action)
        self.snake.insert(0, self.head.coordinates)

        reward = 0
        if self.is_collision_ai() or self.gameFrame > 100 * len(self.snake):
            self.gameOver = True
            reward = -10
            return reward, self.gameOver, self.score

        if self.head.coordinates == self.apple.coordinates:
            self.score += 1
            reward = 10
            self._place_apple()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return reward, self.gameOver, self.score

    def is_collision_ai(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt.coordinates in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(Colors.BLACK.value)

        for pt in self.snake:
            pygame.draw.rect(self.display, Colors.GREEN2.value, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(
            self.display, Colors.GREEN1.value, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE)
        )
        pygame.draw.rect(
            self.display, Colors.RED.value, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE)
        )

        text = self.font.render("Score: " + str(self.score), True, Colors.WHITE.value)
        self.display.blit(text, [WIDTH / 2 - (BLOCK_SIZE * 2), 0])
        pygame.display.flip()

    def _move_ai(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if action[0] == 1:
            # print("go left")
            new_direction = clock_wise[(idx - 1) % 4]

        elif action[1] == 1:
            # print("go straight")
            new_direction = clock_wise[idx]

        else:
            # print("go right")
            new_direction = clock_wise[(idx + 1) % 4]

        self.direction = new_direction

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
