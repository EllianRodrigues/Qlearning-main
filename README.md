# Q-Learning – Projeto de Aprendizado por Reforço

Este projeto implementa o algoritmo **Q-Learning** para ensinar um agente a controlar o personagem **Amongois** em um jogo. O objetivo é que o agente aprenda, por tentativa e erro, o melhor caminho para alcançar o **bloco preto**, evitando quedas e minimizando penalidades.

---

## Como Executar o Projeto

### 1. Inicie o Jogo

- Navegue até a pasta onde o executável do jogo está localizado.
- Abra o arquivo `.exe` para iniciar o servidor local do jogo.

> Isso abrirá uma janela com o ambiente do jogo. O agente será controlado pelo script Python via socket.

### 2. Execute o Script de Treinamento

- No terminal, com o ambiente Python ativado, execute:

```bash
python treinamento.py
```

O script irá:

- Conectar ao servidor do jogo.
- Carregar (ou continuar atualizando) a Q-table salva no arquivo `resultado.txt`.
- Treinar o agente através de episódios infinitos até ser interrompido manualmente.
- Salvar a Q-table a cada episódio no arquivo `resultado.txt`.

> O próprio arquivo `treinamento.py` contém, ao final, um script de simulação comentado. Basta descomentar para testar a política aprendida (com `epsilon = 0`) sem mais treinamento.

---

## Como Funciona o Q-Learning

O Q-Learning é uma técnica de **aprendizado por reforço**. O agente interage com o ambiente e aprende, por tentativa e erro, a melhor ação a tomar em cada estado com base nas recompensas que recebe.

A estratégia segue a equação de Bellman:

```
Q(s, a) ← (1 - α) * Q(s, a) + α * (reward + γ * max(Q(s', a')))
```

- `α` (alpha): taxa de aprendizado — quanto o agente aprende a cada iteração.
- `γ` (gamma): fator de desconto — quanto ele valoriza recompensas futuras.
- `reward`: recompensa recebida pela ação.
- `s` / `s'`: estado atual e estado seguinte.
- `a`: ação tomada.

O agente usa uma **Q-table** para armazenar o valor esperado de cada ação em cada estado. Com o tempo, ele aprende quais ações o levam mais rapidamente ao objetivo (recompensa +300) e evita caminhos que levam à morte (recompensa -100).

---

## Estratégia de Aprendizado

- **Estados** são representados por números inteiros (convertidos do binário do jogo que indica a posição e direção do personagem).
- **Ações disponíveis:** `"left"`, `"right"` e `"jump"`.
- **Recompensas:**
  - Recompensas negativas (ex: `-14`) se o personagem avança sem sucesso.
  - Recompensa positiva de `300` se alcançar o objetivo.
  - Recompensa de `-100` se morrer (cair no vazio).

### Política Epsilon-Greedy:

- O agente escolhe uma ação aleatória com probabilidade `epsilon` (exploração).
- Caso contrário, escolhe a melhor ação segundo a Q-table (exploração).

### Decaimento e Reinício de `epsilon`:

- `epsilon` começa em `0.2` e decai gradualmente (`decay_rate = 0.995`) até `0.05`.
- Quando chega ao mínimo, ele é **reiniciado para `0.5`**, permitindo novas explorações e evitando estagnação.

---

## 🗂️ Arquivos do Projeto

| Arquivo         | Descrição |
|------------------|-----------|
| `treinamento.py` | Script principal que realiza o treinamento do agente. Inclui, ao final, um bloco comentado com o modo de simulação para avaliação da política aprendida. |
| `connection.py`  | Interface com o jogo: conecta ao servidor e envia/recebe ações e estados. |
| `resultado.txt`  | Arquivo com a Q-table aprendida. Salvo e atualizado automaticamente após cada episódio. |

---

## ⚙️ Hiperparâmetros do Algoritmo

| Parâmetro                       | Valor  |
|---------------------------------|--------|
| `alpha` (taxa de aprendizado)   | 0.6    |
| `gamma` (fator de desconto)     | 0.9    |
| `epsilon` inicial               | 0.2    |
| `min_epsilon`                   | 0.05   |
| `decay_rate`                    | 0.995  |
| `epsilon_reset`                 | 0.5    |

---

## Resultados

- Em testes de simulação (com `epsilon = 0`), o agente atingiu o objetivo em:
  - ✅ 11 de 20 episódios (teste 1)
  - ✅ 15 de 20 episódios (teste 2)

Esses resultados indicam que a política aprendida é eficaz, mesmo sem atingir 100% de sucesso.

---

## Entregáveis

- `treinamento.py`
- `connection.py`
- `resultado.txt` (Q-table aprendida)
- `video.mp4` (apresentação do projeto e execução da política)

---

## Grupo

- Ellian dos Santos Rodrigues
- Guilherme Ribeiro Costa Carvalho
- Guilherme Cezar Menezes Siqueira