from connection import connect, get_state_reward
import random
import numpy as np

# Conecta ao jogo
server_socket = connect(2037)

# Carrega a Q-table existente
utility_matrix = np.loadtxt('resultado.txt')
print("✅ Matriz de utilidade carregada.")

np.set_printoptions(precision=6)

actions = ["left", "right", "jump"]

# Hiperparâmetros
alpha = 0.6               # taxa de aprendizado
gamma = 0.9               # fator de desconto
epsilon = 0.2             # taxa de exploração inicial
min_epsilon = 0.05        # mínimo para epsilon
decay_rate = 0.995        # taxa de decaimento por passo

# Estatísticas
successes = 0
episodes = 0

while True:
    print(f"\n Iniciando episódio {episodes + 1}")
    state = 0
    reward = -14
    total_reward = 0

    while True:
        print(f"\nEstado atual: {state}")
        print(f"Taxa de exploração (ε): {epsilon:.3f}")

        # Escolha da ação
        if random.random() < epsilon:
            action_index = random.randint(0, 2)
            chosen_action = actions[action_index]
            print(f"Ação escolhida ALEATÓRIA: {chosen_action}")
        else:
            action_index = np.argmax(utility_matrix[state])
            chosen_action = actions[action_index]
            print(f"Ação escolhida pelo AGENTE: {chosen_action}")

        # Executa ação
        state_info, reward = get_state_reward(server_socket, chosen_action)
        next_state = int(state_info[2:], 2)
        total_reward += reward

        # Atualiza Q-table (Bellman)
        old_value = utility_matrix[state][action_index]
        next_max = np.max(utility_matrix[next_state])
        utility_matrix[state][action_index] = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)

        print(f"Recompensa: {reward}")
        print(f"Próximo estado: {next_state}")
        print(f"Valor Q antes: {old_value:.6f}")
        print(f"Valor Q depois: {utility_matrix[state][action_index]:.6f}")

        # Atualiza estado
        state = next_state

        # Atualiza epsilon
        epsilon = max(min_epsilon, epsilon * decay_rate)
        if epsilon == min_epsilon:
            epsilon = 0.5  # reinicia se chegar no mínimo

        # Termina episódio se morrer ou chegar no objetivo
        if reward == -100:
            print("Personagem morreu")
            break
        elif reward == 300:
            print("Objetivo atingido!")
            successes += 1
            break

    # Salva Q-table após cada episódio
    np.savetxt('resultado.txt', utility_matrix, fmt="%.6f")

    episodes += 1
    print(f"Episódios finalizados: {episodes} | Sucessos: {successes} | Taxa de acerto: {(successes / episodes) * 100:.2f}%")

'''
# Script de teste com a Q-table aprendida

from connection import connect, get_state_reward
import numpy as np

# Conecta ao jogo
server_socket = connect(2037)

# Carrega a Q-table aprendida
utility_matrix = np.loadtxt('resultado.txt')
print("Q-table carregada com sucesso para simulação.")

np.set_printoptions(precision=6)
actions = ["left", "right", "jump"]

# Parâmetros da simulação
exploration_rate = 0.0  # zero exploração
max_episodes = 20
successes = 0

for episode in range(max_episodes):
    print(f"\nEpisódio {episode + 1}")
    state = 0
    reward = -14
    steps = 0

    while True:
        print(f"\n Estado atual: {state}")
        print(f"Ação escolhida: ", end="")

        # Escolhe a melhor ação segundo a Q-table
        action_index = np.argmax(utility_matrix[state])
        action = actions[action_index]
        print(f"{action}")

        state_info, reward = get_state_reward(server_socket, action)
        print(f"Recompensa: {reward}, Novo estado (binário): {state_info}")

        next_state = int(state_info[2:], 2)
        state = next_state
        steps += 1

        if reward == 300:
            print(f"\nObjetivo atingido em {steps} passos!")
            successes += 1
            break

        if reward == -100:
            print(f"\nPersonagem morreu após {steps} passos.")
            break

# Resultado final
print("\nRESULTADO DA SIMULAÇÃO FINAL")
print(f"Total de episódios: {max_episodes}")
print(f"Total de sucessos (chegou ao objetivo): {successes}")
print(f"Porcentagem de sucesso: {(successes / max_episodes) * 100:.2f}%")
'''