import pygame
from snake_game import SnakeGame
from snake_game_ai import SnakeGameAI
from trained_play import play_game_with_trained_model
from agent import Agent
from training import train

# =============================  AI TRAIN  =================================
# game = SnakeGameAI()
# agent = Agent()
# train(agent, game)

# =============================  AI PLAY  =================================
while True:
    play_game_with_trained_model("model/model.pth")

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
