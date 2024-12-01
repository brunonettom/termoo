import requests
import re
from lxml import html  
import csv
import os
import json
import time  # para adicionar delay entre as requisições

def carrega_palavra_secreta():
    url = "http://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1"
    resposta = requests.get(url)
    elemento = html.fromstring(resposta.content)
    palavra_secreta = elemento.xpath('//div[@style="font-size:3em; color:#6200C5;"]/text()')
    palavra_secreta = palavra_secreta[0].strip()
    return palavra_secreta

def salva_palavra_arquivo(palavra, nome_arquivo='palavras_aleatorias.csv'):
    # Verifica se o arquivo já existe
    arquivo_existe = os.path.exists(nome_arquivo)
    
    # Abre o arquivo em modo append ('a')
    with open(nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        
        # Se o arquivo não existia, escreve o cabeçalho
        if not arquivo_existe:
            writer.writerow(['palavra'])
        
        # Escreve a palavra
        writer.writerow([palavra])

def coleta_palavras_continuamente(intervalo=0):
    print("Coletando palavras... Pressione Ctrl+C para parar.")
    try:
        while True:
            # Carrega uma nova palavra
            palavra = carrega_palavra_secreta()
            
            # Salva no arquivo
            salva_palavra_arquivo(palavra)
            
            # Mostra a palavra coletada
            print(f"Palavra coletada: {palavra}")
            
            # Espera um pouco antes de fazer a próxima requisição
            time.sleep(intervalo)
            
    except KeyboardInterrupt:
        print("\nColeta de palavras finalizada!")

# Executa o programa
if __name__ == "__main__":
    coleta_palavras_continuamente()