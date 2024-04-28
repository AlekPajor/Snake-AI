import matplotlib.pyplot as plt
from IPython import display
from snake_game_ai import SnakeGameAI
from agent import Agent

plt.ion()


def plotTraining(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.plot(scores),
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


def train(agent, game):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = agent
    game = game
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
            plotTraining(plot_scores, plot_mean_scores)