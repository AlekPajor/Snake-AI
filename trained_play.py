import pygame
import torch
from snake_game_ai import SnakeGameAI
from agent import Agent
from model import QNet


def play_game_with_trained_model(model_path):
    game = SnakeGameAI()
    agent = Agent()

    model = QNet(input_size=11, hidden_size=256, output_size=3)
    model.load_state_dict(torch.load(model_path))
    agent.model = model

    # Ustawienie games_number na 120 zeby uniknac losowych ruchow
    agent.games_number = 120

    while not game.gameOver:
        # Pobranie stanu gry
        state = agent.get_state(game)

        # Uzyskanie decyzji od modelu
        action = agent.get_action(state)

        # Wykonanie kroku gry na podstawie akcji wygenerowanej przez model
        reward, game.gameOver, score = game.play_step_ai(action)

        # Uzyskanie następnego stanu gry
        next_state = agent.get_state(game)

        # Zapamiętanie doświadczenia
        agent.remember(state, action, reward, next_state, game.gameOver)

        # Aktualizacja stanu
        state = next_state

        # Aktualizacja interfejsu użytkownika
        game._update_ui()

        # Zatrzymanie gry na pewien czas
        pygame.time.wait(50)

    # Wyświetlenie wyniku końcowego
    print("Final Score:", score)