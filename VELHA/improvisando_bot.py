import numpy as np
# velha=np.zeros(3,3)

x=1
o=-1


class Velha():

    def __init__(self):
        self.velha=[[0]*3 for _ in range(3)]
        iniciante=input("quem vai começar? (X/o)")
        if iniciante =="o":
            self.jogador=o
        else:
            self.jogador =x
        
        self.vencedor=0

    def acao(self):
        flag_chute_valido=False
        
        while not flag_chute_valido:
            linha_escolhida = int(input("Qual é a linha?"))
            coluna_escolhida = int(input("Qual é a coluna?"))
            if self.velha[linha_escolhida][coluna_escolhida]==0:
                flag_chute_valido=True
            else:
                print('a sua ação não é válida, tente de novo')
        self.velha[linha_escolhida][coluna_escolhida]=self.jogador



    def quem_venceu(self):
        for i_linha in range(len(self.velha)):
            linha = self.velha[i_linha]
            soma_da_linha = 0
            somas_das_colunas = [0, 0, 0]
            somas_das_diagonais = [0, 0]
            for i_item in range(3):
                item_da_linha = linha[i_item]
                soma_da_linha += item_da_linha
                somas_das_colunas[i_item] += item_da_linha
                if i_item == i_linha:
                    somas_das_diagonais[0] += item_da_linha
                if 2 - i_linha == i_item:
                    somas_das_diagonais[1] += item_da_linha

            if any(soma == -3 for soma in somas_das_diagonais):
                self.vencedor = o
            elif any(soma == 3 for soma in somas_das_diagonais):
                self.vencedor = x

            if soma_da_linha == 3:
                self.vencedor = x
            elif soma_da_linha == -3:
                self.vencedor = o

            for soma_da_coluna in somas_das_colunas:
                if soma_da_coluna == 3:
                    self.vencedor = x
                elif soma_da_coluna == -3:
                    self.vencedor = o

        return self.vencedor


    def main(self):
        

        

        while any(0 in linha for linha in self.velha):
            self.acao()
            print(self.velha)
            self.vencedor = self.quem_venceu()
            print ('vencedor:',self.vencedor)
            if not self.vencedor:
                if self.jogador ==x:
                    self.jogador =o
                else:
                    self.jogador =x
                print(f'o jogador é o: {self.jogador}')
            else:
                break
        if self.vencedor:
            print(f'self.vencedor:{self.vencedor}')
        else: print("deu velha")























#     o| |
#      |x|
#      | |x


























if __name__ == "__main__":
    Jogo=Velha()
    Jogo.main()