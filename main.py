import pygame
from snake_game import SnakeGame
from snake_game_ai import SnakeGameAI
from agent import Agent
from training import train

# =============================  AI  =================================
game = SnakeGameAI()
agent = Agent()
train(agent, game)

# ===========================  PLAYER  ==============================
# game = SnakeGame()
# while True:
#     game_over, score = game.play_step()
#     if game_over:
#         break
#
# print("\n===== GAME OVER =====")
# print('Final Score', score)
# pygame.quit()
