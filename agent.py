import torch
import random
import numpy as np
from snake_game_ai import SnakeGameAI
from utils import Direction, Point
from collections import deque
from model import QNet, QTrainer
import training_plot

MAX_MEMORY = 100_000  # maksymalna ilosc elementow
SAMPLE_SIZE = 1000  # ilosc elementow brana do probki
LEARNING_RATE = 0.001


class Agent:
    def __init__(self):
        self.games_number = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)  # deque - kolejka dwustronna
        self.model = QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

    def get_state(self, game):
        head = game.head
        apple = game.apple
        margin = 20  # Promien otoczenia jakie badamy
        surrounding_points = {
            "left": Point(head.x - margin, head.y),
            "right": Point(head.x + margin, head.y),
            "up": Point(head.x, head.y - margin),
            "down": Point(head.x, head.y + margin)
        }

        # sprawdzamy w ktorym z kierunkow obecnie porusza sie snake
        current_direction = {
            "left": game.direction == Direction.LEFT,
            "right": game.direction == Direction.RIGHT,
            "up": game.direction == Direction.UP,
            "down": game.direction == Direction.DOWN
        }

        state = [
            # badamy zagrozenia dla tego co jest przed nami
            (current_direction["right"] and game.is_collision_ai(surrounding_points["right"])) or
            (current_direction["left"] and game.is_collision_ai(surrounding_points["left"])) or
            (current_direction["up"] and game.is_collision_ai(surrounding_points["up"])) or
            (current_direction["down"] and game.is_collision_ai(surrounding_points["down"])),

            # po prawej
            (current_direction["up"] and game.is_collision_ai(surrounding_points["right"])) or
            (current_direction["down"] and game.is_collision_ai(surrounding_points["left"])) or
            (current_direction["left"] and game.is_collision_ai(surrounding_points["up"])) or
            (current_direction["right"] and game.is_collision_ai(surrounding_points["down"])),

            # po lewej
            (current_direction["down"] and game.is_collision_ai(surrounding_points["right"])) or
            (current_direction["up"] and game.is_collision_ai(surrounding_points["left"])) or
            (current_direction["right"] and game.is_collision_ai(surrounding_points["up"])) or
            (current_direction["left"] and game.is_collision_ai(surrounding_points["down"])),

            # Kierunek ruchu
            current_direction["left"],
            current_direction["right"],
            current_direction["up"],
            current_direction["down"],

            # Lokalizacja jedzenia
            apple.x < head.x,  # jedzenie po lewej
            apple.x > head.x,  # jedzenie po prawej
            apple.y < head.y,  # jedzenie na gorze
            apple.y > head.y  # jedzenie na dole
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        # jezeli mamy juz 1000 probek
        if len(self.memory) > SAMPLE_SIZE:
            # losowa probka z pamieci o rozmiarze BATCH SIZE
            sample = random.sample(self.memory, SAMPLE_SIZE)  # lista tupli
        else:
            sample = self.memory

        # rozkladamy tuple
        states = [s[0] for s in sample]
        actions = [s[1] for s in sample]
        rewards = [s[2] for s in sample]
        next_states = [s[3] for s in sample]
        dones = [s[4] for s in sample]
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # losowe ruchy-badanie kompromisow-tradeoff exploration
        self.epsilon = 110 - self.games_number  # bedzie mozna manipulowac poczatkowa wartoscia
        move = [0, 0, 0]
        # im mniejszy bedzie epsilon, tym rzadziej ten warunek bedzie spelniony. Wartosc epsilon moze
        # spasc do wartosci ujemnych. Wtedy nie bedzie losowych ruchow
        if random.randint(0, 200) < self.epsilon:
            direction = random.randint(0, 2)
            move[direction] = 1
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            # model moze zwrocic wektor z niebinarnymi, trzeba z niego wyciagnac max -> 1
            # np. [5.0, 3.1, 0.1] -----> [1,0,0]
            direction = torch.argmax(prediction).item()
            # szukamy indeksu najwiekszej wartosci i konwertuejmy na zwykla wartosc
            move[direction] = 1
        return move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # stan
        state_old = agent.get_state(game)

        # pobieramy ruch na podstawie obecnego stanu
        final_move = agent.get_action(state_old)

        # wykonujemy ruch i pobieramy nowy stan
        reward, done, score = game.play_step_ai(final_move)
        state_new = agent.get_state(game)

        # trenujemy pamiec krotka
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # zapamietanie
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:  # czy game over
            game.reset()
            agent.games_number += 1
            agent.train_long_memory()

            # aktualizacja rekordu
            if score > record:
                record = score
                agent.model.save()
            print('Game', agent.games_number, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.games_number
            plot_mean_scores.append(mean_score)
            training_plot.plot(plot_scores, plot_mean_scores)
