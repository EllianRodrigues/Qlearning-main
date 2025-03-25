# Q-Learning

Este projeto implementa o algoritmo de aprendizado por reforço **Q-Learning** para controlar o personagem **Amongois** em um jogo. O objetivo do agente é aprender o melhor caminho para alcançar o bloco preto (objetivo final) enquanto minimiza as penalidades (recompensas negativas).

---

## **Como Iniciar o Jogo**

1. **Abrir o Executável do Jogo:**
   - Navegue até a pasta onde o executável do jogo está localizado.
   - Abra o arquivo `.exe` para iniciar o servidor do jogo.

2. **Executar o Algoritmo:**
   - Certifique-se de que o arquivo `client.py` está configurado corretamente.
   - No terminal, execute o seguinte comando:
     ```bash
     python client.py
     ```

3. O agente começará a interagir com o jogo automaticamente, aprendendo o melhor caminho para alcançar o objetivo.

---

## **Como Funciona o Algoritmo**

O algoritmo utiliza o método **Q-Learning**, que funciona da seguinte forma:

1. **Estados e Ações:**
   - O estado é representado como um vetor binário que indica a plataforma em que o personagem está e a direção para a qual ele está virado.
   - O agente pode realizar três ações:
     - `"left"`: Girar para a esquerda.
     - `"right"`: Girar para a direita.
     - `"jump"`: Pular para a frente.

2. **Recompensas:**
   - O jogo retorna recompensas negativas (`-1` a `-14`) com base no estado resultante da ação.
   - O objetivo do agente é minimizar essas penalidades e alcançar o bloco preto.

3. **Q-Table (Matriz de Utilidade):**
   - A matriz de utilidade armazena os valores Q para cada combinação de estado e ação.
   - O agente atualiza os valores Q usando a **Equação de Bellman**:
     \[
     Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_a Q(s', a) - Q(s, a) \right]
     \]
     - `s`: Estado atual.
     - `a`: Ação tomada.
     - `r`: Recompensa recebida.
     - `s'`: Próximo estado.
     - `\alpha`: Taxa de aprendizado.
     - `\gamma`: Fator de desconto.

4. **Exploração e Exploração:**
   - O agente escolhe ações com base na política **epsilon-greedy**:
     - Com probabilidade `epsilon`, escolhe uma ação aleatória (exploração).
     - Caso contrário, escolhe a melhor ação com base na Q-Table (exploração).

---

## **Arquivos do Projeto**

- **`client.py`:** Implementação do algoritmo Q-Learning. Este arquivo controla o agente e realiza a comunicação com o servidor do jogo.
- **`connection.py`:** Fornece as funções para conectar ao servidor (`connect`) e enviar ações/receber estados e recompensas (`get_state_reward`).
- **`resultado.txt`:** Arquivo onde a matriz de utilidade (Q-Table) é salva. Ele é criado automaticamente na primeira execução do `client.py`.

---

## **Hiperparâmetros do Algoritmo**

Os hiperparâmetros controlam o comportamento do aprendizado:

- **`learning_rate` (α):** Taxa de aprendizado. Controla o quanto o agente aprende com novas informações. Valor padrão: `0.02`.
- **`discount_rate` (γ):** Fator de desconto. Determina a importância das recompensas futuras. Valor padrão: `0.5`.
- **`exploration_rate` (ε):** Taxa de exploração. Controla a probabilidade de o agente explorar ações aleatórias. Valor inicial: `0.9` (com decaimento gradual).

---

## **Fluxo do Algoritmo**

1. **Conexão com o Servidor:**
   - O `client.py` conecta ao servidor do jogo usando a função `connect`.

2. **Inicialização da Q-Table:**
   - A matriz de utilidade é carregada do arquivo `resultado.txt` ou inicializada com zeros.

3. **Interação com o Ambiente:**
   - O agente escolhe uma ação com base na política epsilon-greedy.
   - A ação é enviada ao servidor, que retorna o próximo estado e a recompensa.

4. **Atualização da Q-Table:**
   - A matriz de utilidade é atualizada usando a equação de Bellman.

5. **Persistência:**
   - A matriz de utilidade é salva no arquivo `resultado.txt` a cada 20 iterações.
