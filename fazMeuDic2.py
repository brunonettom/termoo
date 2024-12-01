import requests
import re
from lxml import html  
import csv
import os
import json
import time
import threading
import random
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

# Lock para sincronizar a escrita no arquivo
arquivo_lock = threading.Lock()
# Semáforo para controlar o número de requisições simultâneas
request_semaphore = threading.Semaphore(2)  # Permite apenas 2 requisições simultâneas

def carrega_palavra_secreta():
    url = "http://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1"
    try:
        with request_semaphore:  # Controla o número de requisições simultâneas
            resposta = requests.get(url)
            elemento = html.fromstring(resposta.content)
            palavra_secreta = elemento.xpath('//div[@style="font-size:3em; color:#6200C5;"]/text()')
            palavra_secreta = palavra_secreta[0].strip()
            return palavra_secreta
    except Exception as e:
        print(f"Erro ao carregar palavra: {e}")
        return None

def salva_palavra_arquivo(palavra, nome_arquivo='palavras_aleatorias.csv'):
    if not palavra:
        return
        
    with arquivo_lock:  # Usa lock para evitar conflitos na escrita
        arquivo_existe = os.path.exists(nome_arquivo)
        
        with open(nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            
            if not arquivo_existe:
                writer.writerow(['palavra'])
            
            writer.writerow([palavra])

def coletor_palavras(thread_id, intervalo_base=2):
    print(f"Thread {thread_id} iniciada")
    while True:
        try:
            # Adiciona um atraso aleatório entre 1 e 3 segundos
            intervalo_atual = intervalo_base + random.uniform(1, 3)
            
            palavra = carrega_palavra_secreta()
            if palavra:
                salva_palavra_arquivo(palavra)
                print(f"Thread {thread_id} coletou: {palavra}")
            
            # Espera o intervalo calculado antes da próxima requisição
            time.sleep(intervalo_atual)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro na thread {thread_id}: {e}")
            time.sleep(intervalo_atual)

def coleta_palavras_paralela(num_threads=10, intervalo_base=2):
    threads = []
    
    print(f"Iniciando coleta com {num_threads} threads paralelas...")
    print("Pressione Ctrl+C para parar.")
    
    try:
        # Inicia as threads com um pequeno delay entre elas
        for i in range(num_threads):
            thread = threading.Thread(
                target=coletor_palavras,
                args=(i+1, intervalo_base),
                daemon=True
            )
            threads.append(thread)
            thread.start()
            # Adiciona um pequeno delay entre o início de cada thread
            time.sleep(0.5)
        
        # Mantém o programa principal rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nEncerrando coleta de palavras...")
        
    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join(timeout=1)
    
    print("Coleta finalizada!")

if __name__ == "__main__":
    # Intervalo base entre requisições por thread (em segundos)
    INTERVALO_BASE = 2
    NUM_THREADS = 10
    
    coleta_palavras_paralela(NUM_THREADS, INTERVALO_BASE)