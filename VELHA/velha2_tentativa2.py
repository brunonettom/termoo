import numpy as np

x=-1
o=1
dos_dois=1000
ninguem=0
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
        # }}
        


    def inicio(self):
        # {{{{ JOGADOR INICIAL
        jogador_atual=str(input('quem começa? (X/o)'))
        if jogador_atual=='o':
            self.jogador_atual=o
        else:
            self.jogador_atual=x
        # JOGADOR INICIAL }}}}#

        # {{{ ESCOLHA A SUPER CÉLULA
        print('ESCOLHA A SUPER CÉLULA:')
        self.super_i_linha=int(input('qual super linha?'))
        self.super_i_coluna=int(input('qual super coluna?'))
        # }}}

        # {{{ VELHA ATUAL
        self.velha_atual=self.super_velha[self.super_i_linha][self.super_i_coluna]
        # }}}
    
    def main(self):
        '''
        Confere a velha escolhida (if not int [x/o/(deu velha = 1000) --> escolha_a_sua_macro_celula()-até que seja valida]  ) --> 
        - pega a velha escolhida --> (if micro celula == 0:) registra a ação do jogador x na velha atual --> 
        confere se deu velha ou alguem venceu (if +-3 in somas --> super celula e super celula representativa = x/o, elif not any (item==0 for item in (linha for velha_atual))
        deu velha --> super celula e  super celula representativa =1000) --> configura a coordenada da próxima micro --> confere se pode --> repete

        até que super:
        confere se deu velha ou alguem venceu (if +-3 in somas --> super celula e super celula representativa = x/o, elif not any (item==0 for item in (linha for velha_atual))

        '''
        self.inicio()
        while self.vitorioso(self.super_representativa)==ninguem:
            self.mostrar_jogo()
            #print(self.super_velha)
            celula_atual=self.super_velha[self.super_i_linha][self.super_i_coluna]

            # {{{ Confere a velha escolhida (if not int [x/o/(deu velha = 1000) --> escolha_a_sua_macro_celula()
            if type(celula_atual)==int:
                self.escolha_a_sua_macro_celula()   #atualiza o super_i_linha e super_i_coluna até que sejam válidos
            
            velha_atual=self.super_velha[self.super_i_linha][self.super_i_coluna]
            

            print('ESCOLHA A MICRO CÉLULA:')
            self.micro_i_linha=int(input('qual micro linha?'))
            self.micro_i_coluna=int(input('qual micro coluna?'))
            
            if velha_atual[self.micro_i_linha][self.micro_i_coluna] !=ninguem:
                self.escolha_a_sua_micro()
            
            velha_atual[self.micro_i_linha][self.micro_i_coluna] = self.jogador_atual
            if self.vitorioso(velha_atual):
                self.super_representativa[self.super_i_linha][self.super_i_coluna]=self.jogador_atual
                self.super_velha[self.super_i_linha][self.super_i_coluna]=self.jogador_atual
                print(f'AGORA A CÉLULA {self.super_i_linha, self.super_i_coluna} é do{self.vitorioso(velha_atual)}  ')
            
            if self.vitorioso(self.super_representativa):
                print(f'AGORA A SUPER CÉLULA {self.super_i_linha, self.super_i_coluna} é do{self.vitorioso(velha_atual)}  ')
            self.jogador_atual*=-1
            self.super_i_coluna=self.micro_i_coluna
            self.super_i_linha=self.micro_i_linha
            #}}}
            
            #confere se deu velha ou alguem venceu (if +-3 in somas --> super celula e super celula representativa = x/o, elif not any (item==0 for item in (linha for velha_atual))
            #deu velha --> super celula e  super celula representativa =1000) {{{{
        print(f'vitorioso:{self.vitorioso(self.super_representativa)}')

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
            return o
        elif 3 in todas_somas:
            return x
        
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
            

    #  # {{{ Confere a velha escolhida (if not int [x/o/(deu velha = 1000) --> escolha_a_sua_macro_celula()
    #     if type(celula_atual)==int:
    #         self.escolha_a_sua_macro_celula()   #atualiza o super_i_linha e super_i_coluna até que sejam válido

    def escolha_a_sua_macro_celula(self):
        celula_atual = self.super_velha[self.super_i_linha][self.super_i_coluna]
        while type(celula_atual)==int:
            print('a sua ação não é válida, tente de novo')
            self.super_i_linha=int(input('qual super linha?'))
            self.super_i_coluna=int(input('qual super coluna?'))

    def escolha_a_sua_micro(self):
        velha_atual=self.super_velha[self.super_i_linha][self.super_i_coluna]
        while velha_atual[self.micro_i_linha][self.micro_i_coluna] !=ninguem:
            print('a sua ação não é válida, tente de novo')
            self.micro_i_linha=int(input('qual micro linha?'))
            self.micro_i_coluna=int(input('qual micro coluna?'))

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
        
        # Índices das micro colunas
        print("     0   1   2       0   1   2       0   1   2")
        
        # Para cada linha do super jogo
        for super_i in range(3):
            # Índice da super linha
            print(f"Super {super_i}")
            
            # Para cada linha das micro velhas
            for i in range(3):
                # Início da linha com índices
                linha = f"  {i}  "  # micro linha
                
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
                        linha += f" {simbolos[celula]} "
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
        print(f"Para jogar:")
        print("1. Escolha a super célula:  Super [0-2]")
        print("2. Escolha a micro célula:  [0-2]")
        
        # Legenda do estado atual
        print(f"\nJogador atual: {simbolos[self.jogador_atual]}")
        print(f"Super célula atual: [{self.super_i_linha}, {self.super_i_coluna}]")
        
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


if __name__ == "__main__":
    Jogo=Super_velha()
    Jogo.main()