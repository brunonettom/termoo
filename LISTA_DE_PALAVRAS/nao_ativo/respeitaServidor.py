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
request_semaphore = threading.Semaphore(1)  # Permite apenas 1 requisição por vez

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
    ]
    return random.choice(user_agents)

def carrega_palavra_secreta(max_retries=3, base_delay=2):
    url = "http://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1"
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    for attempt in range(max_retries):
        try:
            with request_semaphore:
                resposta = requests.get(url, headers=headers, timeout=10)
                resposta.raise_for_status()  # Raises an HTTPError for bad responses
                
                if resposta.status_code == 200:
                    elemento = html.fromstring(resposta.content)
                    palavras = elemento.xpath('//div[@style="font-size:3em; color:#6200C5;"]/text()')
                    
                    if palavras and len(palavras) > 0:
                        palavra_secreta = palavras[0].strip()
                        if palavra_secreta:  # Verifica se a palavra não está vazia
                            return palavra_secreta
                
                # Se chegou aqui, algo deu errado mas não gerou exceção
                print(f"Tentativa {attempt + 1}: Resposta inválida do servidor")
                
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt + 1}: Erro na requisição: {e}")
        except Exception as e:
            print(f"Tentativa {attempt + 1}: Erro inesperado: {e}")
        
        # Calcula o tempo de espera com backoff exponencial
        if attempt < max_retries - 1:  # Não espera após a última tentativa
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Aguardando {delay:.2f} segundos antes da próxima tentativa...")
            time.sleep(delay)
    
    return None

def salva_palavra_arquivo(palavra, nome_arquivo='palavras_aleatorias.csv'):
    if not palavra:
        return
        
    with arquivo_lock:
        arquivo_existe = os.path.exists(nome_arquivo)
        
        with open(nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            
            if not arquivo_existe:
                writer.writerow(['palavra'])
            
            writer.writerow([palavra])

def coletor_palavras(thread_id, intervalo_base=5):
    print(f"Thread {thread_id} iniciada")
    falhas_consecutivas = 0
    
    while True:
        try:
            # Adiciona um atraso maior se houver falhas consecutivas
            intervalo_atual = intervalo_base * (1.5 ** falhas_consecutivas)
            intervalo_atual += random.uniform(1, 3)
            
            palavra = carrega_palavra_secreta()
            if palavra:
                salva_palavra_arquivo(palavra)
                print(f"Thread {thread_id} coletou: {palavra}")
                falhas_consecutivas = 0  # Reset o contador de falhas
            else:
                falhas_consecutivas += 1
                print(f"Thread {thread_id}: Falha ao coletar palavra")
            
            time.sleep(intervalo_atual)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            falhas_consecutivas += 1
            print(f"Erro na thread {thread_id}: {e}")
            time.sleep(intervalo_atual)

def coleta_palavras_paralela(num_threads, intervalo_base):
    threads = []
    
    print(f"Iniciando coleta com {num_threads} threads paralelas...")
    print("Pressione Ctrl+C para parar.")
    
    try:
        for i in range(num_threads):
            thread = threading.Thread(
                target=coletor_palavras,
                args=(i+1, intervalo_base),
                daemon=True
            )
            threads.append(thread)
            thread.start()
            # Maior delay entre início das threads
            time.sleep(1)
        
        while True:
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nEncerrando coleta de palavras...")
        
    for thread in threads:
        thread.join(timeout=1)
    
    print("Coleta finalizada!")

if __name__ == "__main__":
    # Configurações mais conservadoras
    INTERVALO_BASE = 0.1  # 5 segundos entre requisições
    NUM_THREADS = 15    # Apenas 3 threads
    
    coleta_palavras_paralela(NUM_THREADS, INTERVALO_BASE)