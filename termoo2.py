from datetime import datetime
import numpy as np
from wordfreq import word_frequency, top_n_list
from listaDePalavras2 import listaDePalavras2
from listaDePalavras3 import listaDePalavras3
import requests
import time

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
        self.dicionarioTodo=listaDePalavras3
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
        self.lChavesEscolhidasOriginais = []
        self.lChavesPossiveis = []
        self.palavrasAcertadasConfere=[]
        self.palavrasAcertadas = set()
        self.historicoColunas = {}
        self.flagChuteValido=True
    
    def chavesPossiveis(self):
        lChavesPossiveis = []
        for palavra in self.dicionarioTodo:
            if len(palavra) == self.nLetras:
                lChavesPossiveis.append(palavra)
        return lChavesPossiveis

    def chavesEscolhidas(self, lChavesPossiveis):
        return self.carrega_palavra_secreta()
        # lChavesEscolhidas = []
        # for _ in range(self.nPalavras):
        #     iDaChaveEscolhida = np.random.randint(0, len(lChavesPossiveis))
        #     chaveEscolhida = lChavesPossiveis[iDaChaveEscolhida]
        #     lChavesEscolhidas.append(chaveEscolhida)
        #     del lChavesPossiveis[iDaChaveEscolhida]
        return lChavesEscolhidas

    
    
    def carrega_palavra_secreta(self):
        url = "http://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1"
        horario_inicio = datetime.now()
        lChavesEscolhidas = []
        iteracoes=0
        frequencia=0
        temposDeDemora=[]
        demoras=[]
        # somaTempo=0
        for iPalavra in range(self.nPalavras):
            while True:
                resposta = requests.get(url)
                elemento = html.fromstring(resposta.content)
                palavra_secreta = elemento.xpath('//div[@style="font-size:3em; color:#6200C5;"]/text()')[0].strip()
                duracao = datetime.now() - horario_inicio
                segundos = duracao.total_seconds()
                # Se a palavra tiver o número correto de letras, adicione à lista
                if len(palavra_secreta) == self.nLetras and not palavra_secreta in lChavesEscolhidas:
                    if palavra_secreta in self.en:
                        print(f'A PALAVRA {palavra_secreta} É AMERICANA')
                    else:
                        lChavesEscolhidas.append(palavra_secreta)
                        temposDeDemora.append(int(segundos))
                        if len(temposDeDemora)!=0:
                            demoras.append(int(segundos-temposDeDemora[-1]))
                        break  # Sai do loop enquanto

                # Aguarde para evitar requisições rápidas ao site
                # time.sleep(frequencia)
                iteracoes+=1
                print(f'N ITERAÇÕES: {iteracoes}')
                
                print(f'TEMPO DECORRIDO NA CRIAÇÃO DAS CHAVES ATÉ AGORA: {segundos:.1f}')
                # somaTempo+=segundos
                # faltamNPalavras=self.nPalavras - len(self.lChavesEscolhidas)
                # print (f'\n\nFALTAM {faltamNPalavras} CHUTES')
                
                
                #     print (f'TEMPO POR CHAVE: {tempoPorChave} segundos')
                #     print (f' TEMPO QUE FALTA: {faltamNPalavras*tempoPorChave}')
                if len(temposDeDemora)!=0:
                    print(f'TEMPOS DE DEMORA:{temposDeDemora}')
                if len(demoras)!=0:
                    print(f'DEMORAS: {demoras}')
                    print(self.verde+f'MÉDIA DE DEMORAS: {int(sum(demoras)/(len(demoras)))}'+self.cinza)
                print('\nCHAVES ESCOLHIDAS AGORA',lChavesEscolhidas)
                print(self.amarelo+f'Quantas chaves já foram criadas:{len(lChavesEscolhidas)}'+self.cinza)

                # print("ITERACOES:",iteracoes)
                
                # print("TEMPO:",f'{segundos:.1f} segundos')
                # print(f"MÉDIA POR CILO: {somaTempo/iteracoes:.1f}")
        # self.tempoPrasChaves=segundos
        print(self.vermelho+f'FINAAAAAAAAAAAAAAAALLLLL:::'+self.cinza)
        print(f'TEMPOS DE DEMORA:{temposDeDemora}')
        print(self.verde+f'MÉDIA DE DEMORAS: {int(sum(demoras)/(len(demoras)))}'+self.cinza)
        print('\nCHAVES ESCOLHIDAS AGORA',lChavesEscolhidas)
        print(self.amarelo+f'Quantas chaves já foram criadas:{len(lChavesEscolhidas)}'+self.cinza)

        print('CHAVES ESCOLHIDAS AGORA',lChavesEscolhidas)
        print(self.amarelo+f'Quantas chaves foram criadas no total:{len(lChavesEscolhidas)}'+self.cinza)
        return lChavesEscolhidas

    
    
    def listaDeCorDoChute(self, chute, chave):
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

            print(self.amarelo + f"CHAVES ESCOLHIDAS : {', '.join(palavraSobrante.upper() for palavraSobrante in palavrasSobrantes)}" + self.cinza)
            if len(self.palavrasAcertadasConfere)!=0:
                print(self.verde + f"PALAVRAS ACERTADAS : {', '.join(palavraAcertada.upper() for palavraAcertada in self.palavrasAcertadasConfere)}" + self.cinza)
            
            #PALAVRAS ERRADAS
            lPalavrasErradas=[]
            for palavraChutada in self.palavrasChutadas: 
                if palavraChutada not in self.palavrasAcertadasConfere:
                    lPalavrasErradas.append(palavraChutada)
            if len(lPalavrasErradas)!=0:
                print(self.vermelho + f"PALAVRAS ERRADAS : {', '.join(palavrasErrada.upper() for palavrasErrada in lPalavrasErradas)}" + self.cinza)
            
            
            
            if chute in self.lChavesEscolhidas:
                print(self.verde+f"\nParabéns! Você acertou a palavra '{chute}'!".upper()+self.cinza)
                self.palavrasAcertadasConfere.append(chute)
                self.lChavesEscolhidas.remove(chute)
                self.palavrasAcertadas.add(chute)
                
                if not self.lChavesEscolhidas:
                    print(self.verde+"\n\nVocê acertou todas as palavras! Parabéns!".upper())
                    break
                    
        if self.nLinhasFaltantes == 0:
            print(f"Suas vidas acabaram! As palavras eram: {', '.join(self.lChavesEscolhidasOriginais)}")

    def fazChaves(self):
        # self.nChutesTotais = int(input("Quantos chutes você quer? "))
        self.nLetras = int(input("Quantas letras você quer por palavra? "))
        self.nPalavras = int(input("Quantas palavras? "))
        self.nChutesTotais=self.nLetras+1
        self.nChutesTotais+=self.nPalavras-1
        print("chutes TOTAIS",self.nChutesTotais)
        

        self.lChavesPossiveis = self.chavesPossiveis()
        if not self.lChavesPossiveis:
            print("Nenhuma palavra encontrada com o número de letras especificado.")
            return False
            
        if self.nPalavras > len(self.lChavesPossiveis):
            print(f"Só existem {len(self.lChavesPossiveis)} palavras possíveis com {self.nLetras} letras.")
            self.nPalavras = len(self.lChavesPossiveis)
            
        self.lChavesEscolhidas = self.chavesEscolhidas(self.lChavesPossiveis)
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










import requests
import re
from lxml import html  
import csv,os,json


    
    