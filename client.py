from connection import connect, get_state_reward
import random as randomizer
import numpy as np

# Conexão com o servidor
server_socket = connect(2037)

# Carregar ou inicializar a matriz de utilidade
try:
    utility_matrix = np.loadtxt('resultado.txt')
    print("Matriz de utilidade carregada com sucesso.")
except OSError:
    print("Arquivo resultado.txt não encontrado. Inicializando matriz de utilidade.")
    utility_matrix = np.zeros((96, 3))  # 96 estados x 3 ações

np.set_printoptions(precision=6)

actions = ["left", "right", "jump"]  # Lista de ações possíveis

initial_state = 0  # Estado inicial
initial_reward = -14  # Recompensa inicial

learning_rate = 0.02  #Taxa de aprendizado (alpha)
discount_rate = 0.5  # Fator de desconto (gamma)
exploration_rate = 0.0  # Taxa de exploração inicial (epsilon)

save_counter = 0 # controlar frequência de salvamento

while True:
    print(f"Estado atual do agente: {initial_state}")

    if exploration_rate > 0.35:
        exploration_rate -= 0.001
    print(f"Taxa de exploração atual: {exploration_rate:.3f}")

    if randomizer.random() < exploration_rate:
        action_index = randomizer.randint(0, 2)
        chosen_action = actions[action_index]
        print(f"Ação escolhida ALEATORIAMENTE: {chosen_action}")
    else:
        action_index = np.argmax(utility_matrix[initial_state])
        chosen_action = actions[action_index]
        print(f"Ação escolhida pelo AGENTE: {chosen_action}")

    # Executar a ação e obter o próximo estado e recompensa
    state_info, reward = get_state_reward(server_socket, chosen_action)
    print(f"Recompensa recebida: {reward}, Estado retornado: {state_info}")

    # Processar o estado retornado
    processed_state = int(state_info[2:], 2)
    next_state = processed_state
    print(f"Próximo estado processado: {next_state}")

    # equação de Bellman
    print(f"Valor Q antes da atualização: {utility_matrix[initial_state][action_index]:.6f}")
    utility_matrix[initial_state][action_index] += learning_rate * (
        reward + discount_rate * max(utility_matrix[next_state]) - utility_matrix[initial_state][action_index]
    )
    print(f"Valor Q após a atualização: {utility_matrix[initial_state][action_index]:.6f}")

    # Atualizar o estado e a recompensa atuais
    initial_state = next_state
    initial_reward = reward

    # Incrementar o contador de salvamento
    save_counter += 1

    if save_counter == 20:
        np.savetxt('resultado.txt', utility_matrix, fmt="%.6f")
        save_counter = 0