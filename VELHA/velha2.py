import numpy as np
# velha=np.zeros(3,3)

x=1
o=-1


class Velha():

    def _init_(self):
        self.super_representativa_velha=[[0]*3 for _ in range(3)]
        self.micro_velha0=[[0]*3 for _ in range(3)]

        self.super_velha0=[[self.micro_velha0.copy()]*3 for _ in range(3)]
        self.super_velha = (self.super_velha0.copy())
        iniciante=input("quem vai começar? (X/o)")
        
        if iniciante =="o":
            self.jogador=o
        else:
            self.jogador =x
        
        self.super_vencedor=0
        
        self.estado='escolha_super_celula'

        self.estados={'escolha_super_celula':self.escolha_super_celula,
                      'acao_micro':self.acao_micro,
                      'quem_venceu_micro':self.quem_venceu_micro
                      'micro_deu_velha':self.micro_deu_velha
                      
                      }

    def acao_micro(self, i_linha_velha_atual,i_coluna_velha_atual):
        flag_chute_valido=False
        velha_atual=self.super_velha[i_linha_velha_atual][i_coluna_velha_atual]
        while not flag_chute_valido:
            linha_escolhida = int(input("Qual é a linha?"))
            coluna_escolhida = int(input("Qual é a coluna?"))
            if [linha_escolhida][coluna_escolhida]==0:
                flag_chute_valido=True
            else:
                print('a sua ação não é válida, tente de novo')
        velha_atual[linha_escolhida][coluna_escolhida]=self.jogador
        self.super_velha[i_linha_velha_atual][i_coluna_velha_atual] = velha_atual
        return linha_escolhida,coluna_escolhida


    def quem_venceu_micro(self, i_linha_velha_atual, i_coluna_velha_atual):
        velha_atual = self.super_velha[i_linha_velha_atual][i_coluna_velha_atual]
        somas_das_linhas = [0,0,0]
        somas_das_colunas = [0, 0, 0]
        somas_das_diagonais = [0, 0]
        micro_vencedor=0
        for i_linha in range(len(velha_atual)):
            linha = velha_atual[i_linha]
            for i_item in range(len(linha)):
                item_da_linha = linha[i_item]
                somas_das_linhas[i_linha] += item_da_linha
                somas_das_colunas[i_item] += item_da_linha
                if i_item == i_linha:
                    somas_das_diagonais[0] += item_da_linha
                if 2 - i_linha == i_item:
                    somas_das_diagonais[1] += item_da_linha
        #diagonais
        if any(soma == -3.0 for soma in somas_das_diagonais):
            micro_vencedor = o
        elif any(soma == 3.0 for soma in somas_das_diagonais):
            micro_vencedor = x
        #linhas
        for soma_da_linha in somas_das_linhas:
            if soma_da_linha == 3.0:
                micro_vencedor = x
            elif soma_da_linha == -3.0:
                micro_vencedor = o
        #colunas
        for soma_da_coluna in somas_das_colunas:
            if soma_da_coluna == 3.0:
                micro_vencedor = x
            elif soma_da_coluna == -3.0:
                micro_vencedor = o
        
        if self.micro_deu_velha(velha_atual):
            self.flag_escolha_outra_super_celula=True
        #se vencer --> x ou o, se ninguem vencer --> 0, se deu empate -->1000 e nao pode mais ser acessada --> escolha uma celula
        self.super_representativa_velha[i_linha_velha_atual][i_coluna_velha_atual]=micro_vencedor
        
        # return micro_vencedor
    def micro_deu_velha(self, velha_atual):
        #velha atual
        if not any(item==0 for item in (linha for linha in velha_atual) ):
            return True

    def super_main(self):
        
        while any(0 in linha for linha in self.super_representativa_velha):
            i_linha_velha_atual, i_coluna_velha_atual = self.acao_micro(i_linha_velha_atual, i_coluna_velha_atual)
            print(self.super_representativa_velha)
            self.vencedor = self.quem_venceu_super()

            print ('vencedor:',self.vencedor)
            if not self.vencedor:
                if self.jogador ==x:
                    self.jogador =o
                else:
                    self.jogador =x
                print(f'o jogador é o: {self.jogador}')
            else:
                break
        if self.flag_escolha_outra_super_celula:

        if self.vencedor:
            print(f'self.vencedor:{self.vencedor}')
        else: print("deu super_velha")








if _name_ == "_main_":
    Jogo=Velha()
    Jogo.main()