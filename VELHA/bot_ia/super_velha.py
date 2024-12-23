import numpy as np
import random
from qbot import Bot, QBot

x = -1
o = 1
dos_dois = 1000
ninguem = 0

class Super_velha():
    def __init__(self):
        self.velha0 = [[0]*3 for _ in range(3)]
        self.super_representativa = [[0]*3 for _ in range(3)]
        self.super_velha = [
            [
                [[0]*3 for _ in range(3)] 
                for _ in range(3)
            ] 
            for _ in range(3)
        ]

    def vitorioso(self, velha):
        soma_linhas = [0, 0, 0]
        soma_colunas = [0, 0, 0]
        soma_diagonais = [0, 0]

        for i_linha in range(len(velha)):
            for i_coluna in range(len(velha[i_linha])):
                item = velha[i_linha][i_coluna]
                soma_linhas[i_linha] += item
                soma_colunas[i_coluna] += item
                if i_coluna == i_linha:
                    soma_diagonais[0] += item
                if 2 - i_linha == i_coluna:
                    soma_diagonais[1] += item

        todas_somas = soma_linhas + soma_colunas + soma_diagonais

        if -3 in todas_somas:
            return x
        elif 3 in todas_somas:
            return o
        
        tem_zero = False
        for linha in velha:
            for item in linha:
                if item == 0:
                    tem_zero = True
                    break
        
        if not tem_zero:
            return dos_dois
        
        return ninguem

    def jogada_bot(self, bot):
        if isinstance(bot, QBot):
            old_state = bot.get_state_key(self.super_velha, self.super_representativa, 
                                        self.super_i_linha, self.super_i_coluna)

        jogada = bot.escolher_jogada(self.super_velha, self.super_representativa, 
                                   self.super_i_linha, self.super_i_coluna)
        
        if jogada is None:
            return False
            
        self.super_i_linha, self.super_i_coluna, self.micro_i_linha, self.micro_i_coluna = jogada
        
        velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
        velha_atual[self.micro_i_linha][self.micro_i_coluna] = self.jogador_atual
        
        resultado_micro = self.vitorioso(velha_atual)
        resultado_macro = None
        
        if resultado_micro != ninguem:
            self.super_representativa[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
            self.super_velha[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
            print(f'BOT venceu a célula {self.super_i_linha, self.super_i_coluna}!')
            resultado_macro = self.vitorioso(self.super_representativa)

        if isinstance(bot, QBot):
            new_state = bot.get_state_key(self.super_velha, self.super_representativa, 
                                        self.micro_i_linha, self.micro_i_coluna)
            reward = bot.get_reward(self.super_velha, jogada, resultado_micro, resultado_macro)
            bot.learn(old_state, jogada, reward, new_state)
        
        self.jogador_atual *= -1
        if resultado_micro == ninguem:
            self.super_i_coluna = self.micro_i_coluna
            self.super_i_linha = self.micro_i_linha
    
        return True

    def fazer_jogada_aleatoria(self):
        velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
        if isinstance(velha_atual, int):
            opcoes = []
            for i in range(3):
                for j in range(3):
                    if not isinstance(self.super_velha[i][j], int):
                        opcoes.append((i, j))
            if opcoes:
                self.super_i_linha, self.super_i_coluna = random.choice(opcoes)
                velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
            else:
                return False

        opcoes = []
        for i in range(3):
            for j in range(3):
                if velha_atual[i][j] == 0:
                    opcoes.append((i, j))
        
        if opcoes:
            mi, mj = random.choice(opcoes)
            velha_atual[mi][mj] = self.jogador_atual
            
            if self.vitorioso(velha_atual):
                self.super_representativa[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
                self.super_velha[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
            
            self.jogador_atual *= -1
            self.super_i_linha = mi
            self.super_i_coluna = mj
            return True
            
        return False

    def treinar_bot(self, n_episodes):
        print("\nIniciando treinamento do bot...")
        epsilon_original = self.bot.epsilon
        self.bot.epsilon = 0.3  # Mais exploração durante treino
        
        for episode in range(n_episodes):
            self.__init__()  # Reset do jogo
            self.jogador_atual = self.bot.simbolo
            self.super_i_linha = random.randint(0, 2)
            self.super_i_coluna = random.randint(0, 2)
            
            while self.vitorioso(self.super_representativa) == ninguem:
                if not self.jogada_bot(self.bot):
                    break
                if not self.fazer_jogada_aleatoria():  # Simula oponente
                    break
                    
            if episode % 1000 == 0:
                print(f"Episódio {episode}/{n_episodes}")
        
        self.bot.epsilon = epsilon_original
        self.bot.save_q_table()
        print("Treinamento concluído!")

    def inicio(self):
        modo = input('Jogar contra BOT? (s/n): ')
        self.modo_bot = modo.lower() == 's'
        
        if self.modo_bot:
            tipo_bot = input('Usar bot com aprendizado? (s/n): ')
            jogador_atual = str(input('Você quer ser X ou O? (X/o): '))
            
            if jogador_atual == 'o':
                self.jogador_atual = o
                if tipo_bot.lower() == 's':
                    self.bot = QBot(x)
                else:
                    self.bot = Bot(x)
            else:
                self.jogador_atual = x
                if tipo_bot.lower() == 's':
                    self.bot = QBot(o)
                else:
                    self.bot = Bot(o)
                    
            if isinstance(self.bot, QBot):
                treinar = input('Deseja treinar o bot? (s/n): ')
                if treinar.lower() == 's':
                    episodios = int(input('Quantos episódios de treino? (recomendado: 10000): '))
                    self.treinar_bot(episodios)
        else:
            jogador_atual = str(input('quem começa? (X/o): '))
            if jogador_atual == 'o':
                self.jogador_atual = o
            else:
                self.jogador_atual = x

        print('ESCOLHA A SUPER CÉLULA:')
        self.super_i_linha = int(input('qual super linha?'))
        self.super_i_coluna = int(input('qual super coluna?'))
        self.velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]

    def mostrar_jogo(self):
        simbolos = {
            0: " ",
            -1: "X",
            1: "O",
            1000: "#"
        }
        
        print("\n=== SUPER JOGO DA VELHA ===\n")
        
        # Índices das super colunas
        print("       Super 0         Super 1         Super 2")
        print("     0   1   2       0   1   2       0   1   2")
        
        # Para cada linha do super jogo
        for super_i in range(3):
            print(f"Super {super_i}")
            
            # Para cada linha das micro velhas
            for i in range(3):
                # Início da linha com índices
                linha = f"  {i}  "
                
                # Para cada super coluna
                for super_j in range(3):
                    # Marca se é a célula atual
                    if super_i == self.super_i_linha and super_j == self.super_i_coluna:
                        linha += ">> "
                    else:
                        linha += "   "
                    
                    # Imprime a linha do micro jogo
                    celula = self.super_velha[super_i][super_j]
                    if isinstance(celula, int):
                        # Se a célula foi conquistada, mantemos o formato do jogo da velha
                        if i == 0:
                            linha += " | | "
                        elif i == 1:
                            linha += f" {simbolos[celula]} | "
                        else:
                            linha += " | | "
                    else:
                        linha += f"{simbolos[celula[i][0]]}|{simbolos[celula[i][1]]}|{simbolos[celula[i][2]]}"
                    
                    if super_i == self.super_i_linha and super_j == self.super_i_coluna:
                        linha += " <<"
                    else:
                        linha += "   "
                    
                    # Separador entre super colunas
                    if super_j < 2:
                        linha += " || "
                print(linha)
                
                # Linhas horizontais dentro de cada micro velha
                if i < 2:
                    linha = "     "
                    for super_j in range(3):
                        if super_i == self.super_i_linha and super_j == self.super_i_coluna:
                            linha += ">> "
                        else:
                            linha += "   "
                        
                        # Sempre mostra as linhas horizontais, mesmo em células conquistadas
                        linha += "-+-+-"
                            
                        if super_i == self.super_i_linha and super_j == self.super_i_coluna:
                            linha += " <<"
                        else:
                            linha += "   "
                        if super_j < 2:
                            linha += " || "
                    print(linha)
            
            # Linha divisória entre super linhas
            if super_i < 2:
                print("     " + "="*61)
                
        print(f"\nJogador atual: {simbolos[self.jogador_atual]}")
        print(f"Super célula atual: [Super {self.super_i_linha}, Super {self.super_i_coluna}]")
        
        # Estado geral do jogo
        print("\nEstado do Super Jogo:")
        print("+-----------+")
        for i in range(3):
            print("|", end=" ")
            for j in range(3):
                valor = self.super_representativa[i][j]
                print(f"{simbolos[valor]} ", end="")
            print("|")
            if i < 2:
                print("|-----------+")
        print("+-----------+")
    def escolha_a_sua_macro_celula(self):
        celula_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
        while isinstance(celula_atual, int):
            print('a sua ação não é válida, tente de novo')
            self.super_i_linha = int(input('qual super linha?'))
            self.super_i_coluna = int(input('qual super coluna?'))
            celula_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]

    def escolha_a_sua_micro(self):
        velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
        while velha_atual[self.micro_i_linha][self.micro_i_coluna] != ninguem:
            print('a sua ação não é válida, tente de novo')
            self.micro_i_linha = int(input('qual micro linha?'))
            self.micro_i_coluna = int(input('qual micro coluna?'))
    def main(self):
        self.inicio()
        
        while self.vitorioso(self.super_representativa) == ninguem:
            self.mostrar_jogo()
            
            if self.modo_bot and self.jogador_atual == self.bot.simbolo:
                print("\nVez do BOT...")
                if not self.jogada_bot(self.bot):
                    break
            else:
                celula_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
                
                if isinstance(celula_atual, int):
                    self.escolha_a_sua_macro_celula()
                
                velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
                
                print('ESCOLHA A MICRO CÉLULA:')
                self.micro_i_linha = int(input('qual micro linha?'))
                self.micro_i_coluna = int(input('qual micro coluna?'))
                
                if velha_atual[self.micro_i_linha][self.micro_i_coluna] != ninguem:
                    self.escolha_a_sua_micro()
                
                velha_atual[self.micro_i_linha][self.micro_i_coluna] = self.jogador_atual
                
                if self.vitorioso(velha_atual):
                    self.super_representativa[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
                    self.super_velha[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
                    print(f'VOCÊ venceu a célula {self.super_i_linha, self.super_i_coluna}!')
                
                self.jogador_atual *= -1
                self.super_i_coluna = self.micro_i_coluna
                self.super_i_linha = self.micro_i_linha
        
        vencedor = self.vitorioso(self.super_representativa)
        self.mostrar_jogo()
        if self.modo_bot:
            if vencedor == self.bot.simbolo:
                print("BOT venceu o jogo!")
            elif vencedor == -self.bot.simbolo:
                print("VOCÊ venceu o jogo!")
            else:
                print("Empate!")
        else:
            if vencedor == o:
                print("O venceu o jogo!")
            elif vencedor == x:
                print("X venceu o jogo!")
            else:
                print("Empate!")

if __name__ == "__main__":
    Jogo = Super_velha()
    Jogo.main()