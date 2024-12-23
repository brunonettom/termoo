import numpy as np
import random

x = -1
o = 1
dos_dois = 1000
ninguem = 0

class Bot:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.oponente = -simbolo
        
    def avaliar_posicao(self, velha):
        # Avalia quão boa é uma posição
        # Retorna um valor: positivo é bom para o bot, negativo é ruim
        valor = 0
        
        # Verifica vitória
        vit = self.verifica_vitoria(velha)
        if vit == self.simbolo:
            return 1000
        elif vit == self.oponente:
            return -1000
        
        # Avalia linhas
        for i in range(3):
            linha = velha[i]
            valor += self.avaliar_sequencia(linha)
        
        # Avalia colunas
        for j in range(3):
            coluna = [velha[i][j] for i in range(3)]
            valor += self.avaliar_sequencia(coluna)
        
        # Avalia diagonais
        diag1 = [velha[i][i] for i in range(3)]
        diag2 = [velha[i][2-i] for i in range(3)]
        valor += self.avaliar_sequencia(diag1)
        valor += self.avaliar_sequencia(diag2)
        
        return valor
    
    def avaliar_sequencia(self, seq):
        # Avalia uma sequência (linha/coluna/diagonal)
        meus = seq.count(self.simbolo)
        dele = seq.count(self.oponente)
        vazios = seq.count(0)
        
        if meus == 2 and vazios == 1:
            return 5  # Quase vitória
        if dele == 2 and vazios == 1:
            return -5  # Bloqueio necessário
        if meus == 1 and vazios == 2:
            return 2  # Potencial
        if dele == 1 and vazios == 2:
            return -2  # Ameaça
        
        return 0
    
    def avaliar_super_jogada(self, super_velha, super_representativa, super_i, super_j, micro_i, micro_j):
        # Avalia uma jogada considerando tanto o micro quanto o macro jogo
        valor = 0
        
        # Simula a jogada no micro jogo
        velha_atual = super_velha[super_i][super_j]
        if isinstance(velha_atual, int):
            return -1000  # Célula já conquistada
            
        velha_teste = [linha[:] for linha in velha_atual]
        velha_teste[micro_i][micro_j] = self.simbolo
        
        # Valor do micro jogo
        valor += self.avaliar_posicao(velha_teste)
        
        # Se a jogada ganha o micro jogo, avalia o impacto no super jogo
        if self.verifica_vitoria(velha_teste) == self.simbolo:
            super_teste = [linha[:] for linha in super_representativa]
            super_teste[super_i][super_j] = self.simbolo
            valor += 100 * self.avaliar_posicao(super_teste)
        
        # Avalia a próxima super célula que será ativada
        proxima_velha = super_velha[micro_i][micro_j]
        if not isinstance(proxima_velha, int):
            valor += 0.5 * self.avaliar_posicao(proxima_velha)
        
        return valor
    
    def escolher_jogada(self, super_velha, super_representativa, super_i_linha, super_i_coluna):
        melhor_valor = float('-inf')
        melhor_jogada = None
        
        # Se precisa escolher nova super célula
        if isinstance(super_velha[super_i_linha][super_i_coluna], int):
            # Avalia todas as super células disponíveis
            for i in range(3):
                for j in range(3):
                    if not isinstance(super_velha[i][j], int):
                        for mi in range(3):
                            for mj in range(3):
                                if super_velha[i][j][mi][mj] == 0:
                                    valor = self.avaliar_super_jogada(super_velha, super_representativa, i, j, mi, mj)
                                    if valor > melhor_valor:
                                        melhor_valor = valor
                                        melhor_jogada = (i, j, mi, mj)
        else:
            # Avalia jogadas na super célula atual
            for i in range(3):
                for j in range(3):
                    if super_velha[super_i_linha][super_i_coluna][i][j] == 0:
                        valor = self.avaliar_super_jogada(super_velha, super_representativa, 
                                                        super_i_linha, super_i_coluna, i, j)
                        if valor > melhor_valor:
                            melhor_valor = valor
                            melhor_jogada = (super_i_linha, super_i_coluna, i, j)
        
        return melhor_jogada

class Super_velha():
    def __init__(self):
        self.velha0 = [[0]*3 for _ in range(3)]
        
        # SUPER VELHAS 0 {{
        # Criando uma nova lista para a super representativa
        self.super_representativa = [[0]*3 for _ in range(3)]
        
        # Criando uma nova lista 3D para a super velha
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

        # Junta todas as somas em uma lista
        todas_somas = soma_linhas + soma_colunas + soma_diagonais

        # Verifica vitória
        if -3 in todas_somas:
            return x
        elif 3 in todas_somas:
            return o
        
        # Verifica empate (se não há mais células vazias)
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
        jogada = bot.escolher_jogada(self.super_velha, self.super_representativa, 
                                   self.super_i_linha, self.super_i_coluna)
        
        if jogada is None:
            return False
            
        self.super_i_linha, self.super_i_coluna, self.micro_i_linha, self.micro_i_coluna = jogada
        
        velha_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
        velha_atual[self.micro_i_linha][self.micro_i_coluna] = self.jogador_atual
        
        if self.vitorioso(velha_atual):
            self.super_representativa[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
            self.super_velha[self.super_i_linha][self.super_i_coluna] = self.jogador_atual
            print(f'BOT venceu a célula {self.super_i_linha, self.super_i_coluna}!')
        
        self.jogador_atual *= -1
        self.super_i_coluna = self.micro_i_coluna
        self.super_i_linha = self.micro_i_linha
        return True

    def inicio(self):
        # Pergunta se quer jogar contra o bot
        modo = input('Jogar contra BOT? (s/n): ')
        self.modo_bot = modo.lower() == 's'
        
        # Escolhe quem começa
        if self.modo_bot:
            jogador_atual = str(input('Você quer ser X ou O? (X/o): '))
            if jogador_atual == 'o':
                self.jogador_atual = o
                self.bot = Bot(x)
            else:
                self.jogador_atual = x
                self.bot = Bot(o)
        else:
            jogador_atual = str(input('quem começa? (X/o): '))
            if jogador_atual == 'o':
                self.jogador_atual = o
            else:
                self.jogador_atual = x

        # Escolha inicial da super célula
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
        
        # Fim do jogo
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