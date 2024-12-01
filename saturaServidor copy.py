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
request_semaphore = threading.Semaphore(2)

# Configurações de backoff
class BackoffConfig:
    def __init__(self):
        self.min_delay = 0  # Delay mínimo inicial
        self.max_delay = 300  # Delay máximo (5 minutos)
        self.current_delay = self.min_delay
        self.backoff_factor = 2  # Fator multiplicativo para backoff
        self.success_streak = 0  # Contador de sucessos consecutivos
        self.required_successes = 5  # Número de sucessos necessários para reduzir o delay
        self.lock = threading.Lock()  # Lock para thread safety

    def increase_delay(self):
        with self.lock:
            self.current_delay = min(self.current_delay * self.backoff_factor, self.max_delay)
            self.success_streak = 0
            return self.current_delay

    def decrease_delay(self):
        with self.lock:
            self.success_streak += 1
            if self.success_streak >= self.required_successes:
                self.current_delay = max(self.current_delay / self.backoff_factor, self.min_delay)
                self.success_streak = 0
            return self.current_delay

    def get_current_delay(self):
        with self.lock:
            return self.current_delay

# Instância global do BackoffConfig
backoff_config = BackoffConfig()

def carrega_palavra_secreta():
    url = "http://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1"
    try:
        with request_semaphore:  # Controla o número de requisições simultâneas
            resposta = requests.get(url)
            
            # Verifica se a requisição foi bem sucedida
            if resposta.status_code == 200:
                elemento = html.fromstring(resposta.content)
                palavra_secreta = elemento.xpath('//div[@style="font-size:3em; color:#6200C5;"]/text()')
                
                if palavra_secreta:
                    palavra_secreta = palavra_secreta[0].strip()
                    # Reduz o delay após sucesso
                    backoff_config.decrease_delay()
                    return palavra_secreta
                else:
                    raise Exception("Palavra não encontrada na página")
            else:
                # Aumenta o delay em caso de erro
                raise Exception(f"Status code: {resposta.status_code}")
                
    except Exception as e:
        # Aumenta o delay em caso de qualquer erro
        novo_delay = backoff_config.increase_delay()
        print(f"Erro ao carregar palavra: {e}. Aumentando delay para {novo_delay:.1f}s")
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

def coletor_palavras(thread_id, intervalo_base=2):
    print(f"Thread {thread_id} iniciada")
    falhas_consecutivas = 0
    max_falhas_consecutivas = 10  # Número máximo de falhas antes de aumentar o tempo de espera
    
    while True:
        try:
            # Obtém o delay atual do backoff
            delay_atual = backoff_config.get_current_delay()
            # Adiciona uma variação aleatória de ±25% ao delay
            variacao = random.uniform(-0.25 * delay_atual, 0.25 * delay_atual)
            delay_final = delay_atual + variacao
            
            palavra = carrega_palavra_secreta()
            if palavra:
                salva_palavra_arquivo(palavra)
                print(f"Thread {thread_id} coletou: {palavra} (delay atual: {delay_atual:.1f}s)")
                falhas_consecutivas = 0  # Reseta o contador de falhas
            else:
                falhas_consecutivas += 1
                if falhas_consecutivas >= max_falhas_consecutivas:
                    print(f"Thread {thread_id}: Muitas falhas consecutivas, aumentando tempo de espera...")
                    backoff_config.increase_delay()
                    falhas_consecutivas = 0
            
            # Espera o delay calculado antes da próxima requisição
            time.sleep(max(delay_final, 1))  # Garante um mínimo de 1 segundo
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro na thread {thread_id}: {e}")
            time.sleep(delay_atual)

def coleta_palavras_paralela(num_threads=10):
    threads = []
    
    print(f"Iniciando coleta com {num_threads} threads paralelas...")
    print("Pressione Ctrl+C para parar.")
    
    try:
        # Inicia as threads com um pequeno delay entre elas
        for i in range(num_threads):
            thread = threading.Thread(
                target=coletor_palavras,
                args=(i+1,),
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
    NUM_THREADS = 10
    coleta_palavras_paralela(NUM_THREADS)