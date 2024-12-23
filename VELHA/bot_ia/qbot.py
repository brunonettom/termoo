# qbot.py

import numpy as np
import pickle
import random
from collections import defaultdict

class Bot:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.oponente = -simbolo
    
    # ... (outros métodos)

class QBot(Bot):
    def __init__(self, simbolo, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        super().__init__(simbolo)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = self.load_q_table()
    
    def get_state_key(self, super_velha, super_representativa, super_i, super_j):
        if isinstance(super_velha, str):
            return super_velha
            
        estado = str(super_representativa)
        estado += f"_{super_i}_{super_j}"
        return estado
    
    def load_q_table(self):
        try:
            with open('q_table.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return defaultdict(lambda: defaultdict(float))
            
    def save_q_table(self):
        with open('q_table.pkl', 'wb') as f:
            pickle.dump(dict(self.q_table), f)
    
    def get_possible_actions(self, super_velha, super_i, super_j):
        if isinstance(super_velha, str):
            return []
            
        actions = []
        if isinstance(super_velha[super_i][super_j], int):
            for i in range(3):
                for j in range(3):
                    if not isinstance(super_velha[i][j], int):
                        for mi in range(3):
                            for mj in range(3):
                                if super_velha[i][j][mi][mj] == 0:
                                    actions.append((i, j, mi, mj))
        else:
            for i in range(3):
                for j in range(3):
                    if super_velha[super_i][super_j][i][j] == 0:
                        actions.append((super_i, super_j, i, j))
        return actions
    
    def escolher_jogada(self, super_velha, super_representativa, super_i_linha, super_i_coluna):
        if random.random() < self.epsilon:
            # Usa estratégia do Bot tradicional
            return Bot.escolher_jogada(self, super_velha, super_representativa, 
                                     super_i_linha, super_i_coluna)
        
        state = self.get_state_key(super_velha, super_representativa, 
                                 super_i_linha, super_i_coluna)
        actions = self.get_possible_actions(super_velha, super_i_linha, super_i_coluna)
        
        if not actions:
            return None
            
        # Combina Q-values com avaliação heurística
        action_values = {}
        for action in actions:
            q_value = self.q_table[state][str(action)]
            heuristic_value = self.avaliar_super_jogada(super_velha, super_representativa, 
                                                       *action) / 1000.0
            combined_value = 0.7 * q_value + 0.3 * heuristic_value
            action_values[action] = combined_value
        
        return max(action_values.items(), key=lambda x: x[1])[0]

    def avaliar_super_jogada(self, super_velha, super_representativa, super_i, super_j, micro_i, micro_j):
        valor = 0
        
        velha_atual = super_velha[super_i][super_j]
        if isinstance(velha_atual, int):
            return -1000
            
        velha_teste = [linha[:] for linha in velha_atual]
        velha_teste[micro_i][micro_j] = self.simbolo
        
        # Aumenta peso do micro jogo
        valor += 10 * self.avaliar_posicao(velha_teste)
        
        if self.verifica_vitoria(velha_teste) == self.simbolo:
            super_teste = [linha[:] for linha in super_representativa]
            super_teste[super_i][super_j] = self.simbolo
            # Aumenta MUITO o peso da vitória no macro jogo
            valor += 1000 * self.avaliar_posicao(super_teste)
        
        return valor
    
    def learn(self, state, action, reward, next_state, super_velha, super_i, super_j):
        old_value = self.q_table[state][str(action)]
        
        # Obtém as ações possíveis para o próximo estado
        next_actions = self.get_possible_actions(super_velha, super_i, super_j)
        next_values = [self.q_table[next_state][str(a)] for a in next_actions]
        next_max = max(next_values) if next_values else 0
        
        # Atualiza o valor Q usando a fórmula do Q-Learning
        new_value = (1 - self.learning_rate) * old_value + \
                self.learning_rate * (reward + self.discount_factor * next_max)
                
        self.q_table[state][str(action)] = new_value

    def get_reward(self, super_velha, action, resultado_micro, resultado_macro=None):
        reward = 0
        
        if resultado_micro == self.simbolo:
            reward += 10
        elif resultado_micro == self.oponente:
            reward -= 10
            
        if resultado_macro is not None:
            if resultado_macro == self.simbolo:
                reward += 100
            elif resultado_macro == self.oponente:
                reward -= 100
        
        _, _, mi, mj = action
        if (mi, mj) == (1, 1):
            reward += 3
        if (mi, mj) in [(0,0), (0,2), (2,0), (2,2)]:
            reward += 2
            
        return reward
