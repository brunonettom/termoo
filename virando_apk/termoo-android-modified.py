# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, NumericProperty
from kivy.utils import get_color_from_hex
from wordfreq import top_n_list
import random
import unicodedata
# Importando sua lista de palavras
from listaDePalavrasFinal_01_12_2024__22_28 import palavras

# Cores do jogo
VERDE = get_color_from_hex('#32CD32')
AMARELO = get_color_from_hex('#FFD700')
CINZA = get_color_from_hex('#808080')
BRANCO = get_color_from_hex('#FFFFFF')

class TermooGame:
    def __init__(self):
        # Usando tanto o wordfreq quanto sua lista personalizada
        self.dicionario = top_n_list('pt', 300000)
        self.palavras_possiveis = [p.lower() for p in palavras if ' ' not in p and '-' not in p]
        self.palavras_chutadas = []
        self.palavras_acertadas = set()
        
    def remover_acentos(self, palavra):
        nfkd = unicodedata.normalize('NFD', palavra)
        sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        return sem_acentos.replace('ç', 'c').replace('Ç', 'C')
    
    def verifica_palavra(self, chute, palavra_chave):
        if len(chute) != len(palavra_chave):
            return None
            
        resultado = ['cinza'] * len(chute)
        palavra_temp = list(palavra_chave)
        
        # Verifica letras verdes
        for i in range(len(chute)):
            if chute[i] == palavra_chave[i]:
                resultado[i] = 'verde'
                palavra_temp[i] = None
        
        # Verifica letras amarelas
        for i in range(len(chute)):
            if resultado[i] == 'cinza' and chute[i] in palavra_temp:
                resultado[i] = 'amarelo'
                palavra_temp[palavra_temp.index(chute[i])] = None
                
        return resultado

class TermooGrid(GridLayout):
    def __init__(self, palavra_chave, **kwargs):
        super().__init__(**kwargs)
        self.cols = len(palavra_chave)
        self.palavra_chave = palavra_chave
        self.rows = 6  # Tentativas
        self.spacing = 2
        self.cells = []
        
        for _ in range(self.rows * self.cols):
            cell = Label(
                text='',
                background_color=CINZA,
                canvas_color=CINZA,
                size_hint=(1, 1)
            )
            self.cells.append(cell)
            self.add_widget(cell)

class TermooTeclado(GridLayout):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.cols = 10
        self.rows = 3
        self.criar_teclado()
        
    def criar_teclado(self):
        letras = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        for letra in letras:
            btn = Button(
                text=letra,
                on_press=self.callback,
                background_normal='',
                background_color=CINZA,
                color=BRANCO
            )
            self.add_widget(btn)

class TermooApp(App):
    def build(self):
        self.game = TermooGame()
        self.n_letras = 5  # Padrão
        self.palavra_chave = self.escolher_palavra()
        self.tentativas_maximas = 6
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Informações do jogo
        info_layout = BoxLayout(size_hint_y=0.1)
        self.info_label = Label(text=f'Tentativas: 0/{self.tentativas_maximas}')
        info_layout.add_widget(self.info_label)
        layout.add_widget(info_layout)
        
        # Grid do jogo
        self.grid = TermooGrid(self.palavra_chave)
        layout.add_widget(self.grid)
        
        # Campo de entrada
        self.entrada = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            on_text_validate=self.verificar_palavra
        )
        layout.add_widget(self.entrada)
        
        # Teclado
        self.teclado = TermooTeclado(self.press_key)
        layout.add_widget(self.teclado)
        
        return layout
    
    def escolher_palavra(self):
        # Escolhe palavras da sua lista personalizada
        palavras_validas = [p for p in self.game.palavras_possiveis if len(p) == self.n_letras]
        palavra = random.choice(palavras_validas)
        return self.game.remover_acentos(palavra.lower())
    
    def press_key(self, instance):
        if len(self.entrada.text) < self.n_letras:
            self.entrada.text += instance.text.lower()
    
    def verificar_palavra(self, instance):
        chute = self.entrada.text.lower()
        if len(chute) != self.n_letras:
            self.mostrar_erro(f"A palavra deve ter {self.n_letras} letras!")
            return
        
        # Verifica se a palavra está no dicionário do wordfreq ou na sua lista
        if chute not in self.game.dicionario and chute not in self.game.palavras_possiveis:
            self.mostrar_erro("Palavra não encontrada no dicionário!")
            return
        
        resultado = self.game.verifica_palavra(chute, self.palavra_chave)
        self.atualizar_grid(chute, resultado)
        self.entrada.text = ''
        
        # Atualiza contador de tentativas
        tentativas = len(self.game.palavras_chutadas)
        self.info_label.text = f'Tentativas: {tentativas}/{self.tentativas_maximas}'
        
        if all(r == 'verde' for r in resultado):
            self.mostrar_vitoria()
        elif tentativas >= self.tentativas_maximas:
            self.mostrar_derrota()
    
    def atualizar_grid(self, chute, resultado):
        linha_atual = len(self.game.palavras_chutadas)
        for i, (letra, cor) in enumerate(zip(chute, resultado)):
            cell = self.grid.cells[linha_atual * self.n_letras + i]
            cell.text = letra.upper()
            if cor == 'verde':
                cell.background_color = VERDE
            elif cor == 'amarelo':
                cell.background_color = AMARELO
            else:
                cell.background_color = CINZA
        
        self.game.palavras_chutadas.append(chute)
    
    def mostrar_erro(self, mensagem):
        popup = Popup(
            title='Erro',
            content=Label(text=mensagem),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
    
    def mostrar_vitoria(self):
        popup = Popup(
            title='Parabéns!',
            content=Label(text=f'Você acertou a palavra: {self.palavra_chave.upper()}!'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
    
    def mostrar_derrota(self):
        popup = Popup(
            title='Fim de Jogo',
            content=Label(text=f'A palavra era: {self.palavra_chave.upper()}'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    Window.clearcolor = (0.9, 0.9, 0.9, 1)
    TermooApp().run()
