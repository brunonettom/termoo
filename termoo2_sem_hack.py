from datetime import datetime
import numpy as np
from wordfreq import word_frequency, top_n_list
from listaDePalavrasFinal_01_12_24 import palavras
import requests
import random
from datetime import datetime
import requests
from lxml import html
import unicodedata


import time

from datetime import datetime
import requests
from lxml import html

import re
from lxml import html  
import csv,os,json
# dicionarioTodo=top_n_list('pt', 300000)
# print(dicionarioTodo)
class Termoo():
    def __init__(self):
        # self.dicionarioTodo = todasAsPalavras
        self.en = top_n_list('en', 100000, wordlist='large')
        self.dicionarioTodo=top_n_list('pt', 300000)
        self.possiveisChaves=palavras
        self.vermelho = '\033[91m'
        self.cinza = "\033[37m"
        self.amarelo = "\033[33m"
        self.verde = "\033[32m"
        self.resetar_cor = "\033[0m"
        self.palavrasChutadas = []
        self.nPalavras = None
        self.nLetras = None
        self.nLinhasFaltantes = None
        self.lChavesEscolhidas = []
        self.palavrasErradas=[]
        self.lChavesEscolhidasOriginais = []
        self.lChavesPossiveis = []
        self.palavrasAcertadasConfere=[]
        self.palavrasAcertadas = set()
        self.historicoColunas = {}
        self.flagChuteValido=True
        self.flagDebuggar=False
        self.flagVerIteracoes=False
    
    def remover_acentos(self, palavra):
        """
        Remove acentos e substitui 'ç' por 'c' na palavra fornecida.
        
        Args:
            palavra (str): A palavra a ser processada.
        
        Returns:
            str: A palavra sem acentos e com 'ç' substituído por 'c'.
        """
        # Normaliza a palavra para decompor caracteres acentuados
        nfkd = unicodedata.normalize('NFD', palavra)
        # Remove os caracteres de marcação de acentuação
        sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        # Substitui 'ç' por 'c'
        sem_acentos = sem_acentos.replace('ç', 'c').replace('Ç', 'C')
        return sem_acentos

    def chavesEscolhidas(self):
        """
        Seleciona aleatoriamente um conjunto de palavras como chaves do jogo.
        
        Returns:
            list: Lista de palavras selecionadas como chaves.
        """
        ChavesEscolhidas = []
        lPreChavesEscolhidas = [word.lower() for word in self.possiveisChaves if ' ' not in word and '-' not in word]
        
        # Garante que a lista lPreChavesEscolhidas tenha palavras suficientes para seleção
        if len(lPreChavesEscolhidas) < self.nPalavras:
            print("Erro: Não há palavras suficientes para selecionar.")
            return []

        for _ in range(self.nPalavras):
            sorteada=random.choice(lPreChavesEscolhidas)
            while len(sorteada) != self.nLetras or sorteada in ChavesEscolhidas:
                sorteada=random.choice(lPreChavesEscolhidas)

            ChavesEscolhidas.append(sorteada)

        self.lChavesEscolhidasOriginais0 = ChavesEscolhidas
        lChavesEscolhidas = [self.remover_acentos(palavra) for palavra in ChavesEscolhidas]
        return lChavesEscolhidas

  
    def listaDeCorDoChute(self, chute, chave):
        if len(chute) != self.nLetras or len(chave) != self.nLetras:
            print(f"Erro: A palavra deve ter exatamente {self.nLetras} letras.")
            return [self.cinza] * self.nLetras, 0
        
        listaDeCorDoChute = [self.cinza] * self.nLetras
        nVerdes = 0
        chuteVAmarelo = list(chave)

        for i in range(self.nLetras):
            if chute[i] == chave[i]:
                listaDeCorDoChute[i] = self.verde
                nVerdes += 1
                chuteVAmarelo[i] = None

        for i in range(self.nLetras):
            if listaDeCorDoChute[i] == self.cinza and chute[i] in chuteVAmarelo:
                listaDeCorDoChute[i] = self.amarelo
                index_amarelo = chuteVAmarelo.index(chute[i])
                chuteVAmarelo[index_amarelo] = None

        return listaDeCorDoChute, nVerdes


    def pintaPalavra(self, chute, listaDeCorDoChute):
        palavraPintada = ""
        for i in range(len(chute)):
            palavraPintada += listaDeCorDoChute[i] + chute[i] + " "
        palavraPintada += self.resetar_cor
        return palavraPintada

    def chuteColorido(self, chute, palavraPintada):
        return palavraPintada

    def trataChute(self, chave, chute):
        listaDeCorDoChute, nVerdes = self.listaDeCorDoChute(chute, chave)
        palavraPintada = self.pintaPalavra(chute, listaDeCorDoChute)
        chuteColorido = self.chuteColorido(chute, palavraPintada)
        return chuteColorido, nVerdes

    def linhaVazia(self):
        return "_ " * self.nLetras + "\n"

    def colunai(self, chave, iColuna):
        
        if chave in self.palavrasAcertadas:
            str = self.verde + f"\nPALAVRA {iColuna + 1} - ACERTADA: {chave.upper()}\n" + self.cinza
            
            return str
    
        
        resultado = f'PALAVRA {iColuna + 1}\n\n'
        
        # Se a palavra já foi acertada, usar o histórico salvo mais as linhas vazias atualizadas
        if chave in self.palavrasAcertadas:
            historico_base = self.historicoColunas.get(iColuna, "")
            # Adicionar as linhas vazias atuais
            for _ in range(self.nLinhasFaltantes):
                historico_base += self.linhaVazia()
            return historico_base
        
        # Processar os chutes normalmente
        nsLetrasVerdes = []
        for chute in self.palavrasChutadas:
            chuteColorido, nVerdes = self.trataChute(chave, chute)
            resultado += chuteColorido + "\n"
            nsLetrasVerdes.append(nVerdes)
            
            # Se este chute acertou a palavra, salvamos o histórico base (sem linhas vazias)
            if chute == chave:
                self.historicoColunas[iColuna] = resultado
                # Adicionar as linhas vazias atuais
                for _ in range(self.nLinhasFaltantes):
                    resultado += self.linhaVazia()
                return resultado
                
        # Se a palavra não foi acertada, adicionar linhas vazias
        for _ in range(self.nLinhasFaltantes):
            resultado += self.linhaVazia()
                
        return resultado

    def fazChutes(self):
        self.nLinhasFaltantes = self.nChutesTotais - len(self.palavrasChutadas) -1
        
        while self.nLinhasFaltantes > 0 and self.lChavesEscolhidas:
            self.nLinhasFaltantes = self.nChutesTotais - len(self.palavrasChutadas)
            
            # print(f'TEMPO PRA CONSEGUIR AS CHAVES {self.tempoPrasChaves:.2f}')
            # print(f'TEMPO PRA CADA CHAVE: {(self.tempoPrasChaves/self.nPalavras):.1f}')
            chute = input("\nDigite um chute: ").lower()
            if chute =="" or not chute:
                print(self.vermelho+"FAÇA UM CHUTE!!!"+self.cinza)
                continue
            if chute == 'desisto' or chute =='q' or chute == 'quit' or chute =='sair':
                self.nLinhasFaltantes=0
                continue
            if len(chute) != self.nLetras:
                print(f"Por favor, digite uma palavra com {self.nLetras} letras.")
                self.flagChuteValido=False
                continue
            if chute not in self.dicionarioTodo:
                self.flagChuteValido=False
                print("Palavra não encontrada no dicionário.")
                continue
                
            self.palavrasChutadas.append(chute)
            print(self.todasAsColunas())
            
            #PALAVRAS SOBRANTES:
            palavrasSobrantes=[]
            for palavraEscolhida in self.lChavesEscolhidasOriginais:
                if palavraEscolhida not in self.palavrasAcertadas:
                    palavrasSobrantes.append(palavraEscolhida)
            
            print(self.vermelho+f"Vidas restantes: {self.nLinhasFaltantes}"+self.cinza) 
            print(self.amarelo+ f"Palavras faltentes: {len(palavrasSobrantes)}"+self.cinza+"\n")


        #CHAVES ESCOLHIDAS
            if not self.flagDebuggar:
                print(self.amarelo + f'NÚMERO DE PALAVRAS QUE FALTAM: {len(palavrasSobrantes)}'+ self.cinza)
            if self.flagDebuggar:
                print(self.amarelo + f"CHAVES ESCOLHIDAS : {', '.join(chaveEscolhida.upper() for chaveEscolhida in palavrasSobrantes)}" + self.cinza)

        #PALAVRAS ACERTADAS
            # print(self.amarelo + f"CHAVES ESCOLHIDAS : {', '.join(palavraSobrante.upper() for palavraSobrante in palavrasSobrantes)}" + self.cinza)
            if len(self.palavrasAcertadasConfere)!=0:
                print(self.verde + f"PALAVRAS ACERTADAS : {', '.join(palavraAcertada.upper() for palavraAcertada in self.palavrasAcertadasConfere)}" + self.cinza)
            
           
            
            
            # TRATA CHUTES
            if chute in self.lChavesEscolhidas:
                print(self.verde+f"\nParabéns! Você acertou a palavra '{chute}'!".upper()+self.cinza)
                self.palavrasAcertadasConfere.append(chute)
                self.lChavesEscolhidas.remove(chute)
                self.palavrasAcertadas.add(chute)
                
                if not self.lChavesEscolhidas:
                    print(self.verde+"\n\nVocê acertou todas as palavras! Parabéns!".upper())
                    break
            else: 
                self.palavrasErradas.append(chute)

             #PALAVRAS ERRADAS

            if len(self.palavrasErradas)!=0:
                print(self.vermelho + f"PALAVRAS ERRADAS : {', '.join(palavrasErrada.upper() for palavrasErrada in self.palavrasErradas)}" + self.cinza)
                    
        if self.nLinhasFaltantes == 0:
            print(f"Suas vidas acabaram! As palavras eram: {', '.join(self.lChavesEscolhidasOriginais0)}".upper())

    def fazChaves(self):
        escolherNChutes=input("Quer escolher quantos chutes quer? (s/N) (y/N)")
        if escolherNChutes=='s' or escolherNChutes=='y':
            self.nChutesTotais = int(input("Quantos chutes você quer? "))
        preNLetras = input("Quantas letras você quer por palavra? (5)")
        if preNLetras=='' or not preNLetras:
            self.nLetras=5
        else:
            self.nLetras = int(preNLetras)
        
        preNPalavras= input("Quantas palavras? ")

        if preNPalavras=='' or not preNPalavras:
            self.nPalavras=2
        else:
            self.nPalavras = int(preNPalavras)
        


        if not(preNPalavras=='s' or preNPalavras=='y'):
            self.nChutesTotais=self.nLetras+1
            self.nChutesTotais+=self.nPalavras-1

        print("chutes TOTAIS",self.nChutesTotais)
        

        self.lChavesEscolhidas = self.chavesEscolhidas()
        self.lChavesEscolhidasOriginais = self.lChavesEscolhidas.copy()
        
        return True

    def todasAsColunas(self):
        resultado = ""
        for iColuna in range(self.nPalavras):
            chave_atual = self.lChavesEscolhidasOriginais[iColuna]
            resultado += self.colunai(chave_atual, iColuna) + "\n"
        return resultado

if __name__ == "__main__":
    termoo = Termoo()
    if termoo.fazChaves():
        termoo.fazChutes()











    
    