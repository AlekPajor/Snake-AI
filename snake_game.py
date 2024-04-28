import pygame
import random
from utils import Direction, Point, Colors

BLOCK_SIZE = 16
WIDTH = BLOCK_SIZE * 32
HEIGHT = BLOCK_SIZE * 32
SPEED = 10


class SnakeGame:
    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head.coordinates,
                      Point(self.head.x - BLOCK_SIZE, self.head.y).coordinates,
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y).coordinates]

        self.score = 0
        self.apple = None
        self._place_apple()
        self.gameInit = pygame.init()
        pygame.display.set_caption('Snake')
        self.font = pygame.font.SysFont('arial', 25)
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.gameOver = False

    def _place_apple(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.apple = Point(x, y)
        if Point(x, y) in self.snake:
            self._place_apple()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN

        self._move(self.direction)
        self.snake.insert(0, self.head.coordinates)

        if self._is_collision():
            self.gameOver = True
            return self.gameOver, self.score

        if self.head.coordinates == self.apple.coordinates:
            self.score += 1
            self._place_apple()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return self.gameOver, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head.coordinates in self.snake[1:]:
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
        self.display.blit(text, [WIDTH/2 - (BLOCK_SIZE*2), 0])
        pygame.display.flip()

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
