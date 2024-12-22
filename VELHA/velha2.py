mport numpy as np
# velha=np.zeros(3,3)

x=1
o=-1


class Velha():

    def _init_(self):
        self.micro_velha0=[[0]*3 for _ in range(3)]
        self.super_velha0=[[self.micro_velha0.copy()]*3 for _ in range(3)]
        self.super_velha = (self.super_velha0.copy())
        iniciante=input("quem vai começar? (X/o)")
        
        if iniciante =="o":
            self.jogador=o
        else:
            self.jogador =x
        
        self.super_vencedor=0
        
    def acao_micro(self, linha_velha_atual,coluna_velha_atual):
        flag_chute_valido=False
        velha_atual=self.super_velha[linha_velha_atual][coluna_velha_atual]
        while not flag_chute_valido:
            linha_escolhida = int(input("Qual é a linha?"))
            coluna_escolhida = int(input("Qual é a coluna?"))
            if [linha_escolhida][coluna_escolhida]==0:
                flag_chute_valido=True
            else:
                print('a sua ação não é válida, tente de novo')
        velha_atual[linha_escolhida][coluna_escolhida]=self.jogador
        self.super_velha[linha_velha_atual][coluna_velha_atual] = velha_atual
        return linha_escolhida,coluna_escolhida


    def quem_venceu_micro(self, linha_velha_atual, coluna_velha_atual):
        velha_atual = self.super_velha[linha_velha_atual][coluna_velha_atual]
        soma_da_linha = 0
        somas_das_colunas = [0, 0, 0]
        somas_das_diagonais = [0, 0]
        micro_vencedor=None
        for i_linha in range(len(velha_atual)):
            linha = velha_atual[i_linha]
            for i_item in range(3):
                item_da_linha = linha[i_item]
                soma_da_linha += item_da_linha
                somas_das_colunas[i_item] += item_da_linha
                if i_item == i_linha:
                    somas_das_diagonais[0] += item_da_linha
                if 2 - i_linha == i_item:
                    somas_das_diagonais[1] += item_da_linha

        if any(soma == -3.0 for soma in somas_das_diagonais):
            micro_vencedor = o
        elif any(soma == 3.0 for soma in somas_das_diagonais):
            micro_vencedor = x
        if soma_da_linha == 3.0:
            micro_vencedor = x
        elif soma_da_linha == -3.0:
            micro_vencedor = o

        for soma_da_coluna in somas_das_colunas:
            if soma_da_coluna == 3.0:
                micro_vencedor = x
            elif soma_da_coluna == -3.0:
                micro_vencedor = o
        
        if not micro_vencedor:
            velha_atual=micro_vencedor
        

        self.super_velha[linha_velha_atual][coluna_velha_atual]= velha_atual
        # return micro_vencedor


    def super_main(self):
      
        while any(0 in linha for linha in self.super_velha):
            linha_velha_atual, coluna_velha_atual = self.acao_micro(linha_velha_atual, coluna_velha_atual)
            print(self.super_velha)
            self.vencedor = self.quem_venceu_micro()
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
        else: print("deu super_velha")








if _name_ == "_main_":
    Jogo=Velha()
    Jogo.main()