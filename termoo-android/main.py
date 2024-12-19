# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from listaDePalavrasFinal_01_12_2024__22_28 import palavras  # Importa sua lista de palavras
import random
import unicodedata

# Cores do jogo
VERDE = get_color_from_hex('#32CD32')
AMARELO = get_color_from_hex('#FFD700')
CINZA = get_color_from_hex('#808080')
BRANCO = get_color_from_hex('#FFFFFF')

class TermooGame:
    def __init__(self):
        self.palavras_possiveis = palavras  # Usa sua lista de palavras
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
        
        # Verifica verdes
        for i in range(len(chute)):
            if chute[i] == palavra_chave[i]:
                resultado[i] = 'verde'
                palavra_temp[i] = None
        
        # Verifica amarelos
        for i in range(len(chute)):
            if resultado[i] == 'cinza' and chute[i] in palavra_temp:
                resultado[i] = 'amarelo'
                palavra_temp[palavra_temp.index(chute[i])] = None
                
        return resultado

class TermooLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

class LetterGrid(GridLayout):
    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        self.cols = size
        self.rows = 6
        self.spacing = 2
        self.cells = []
        
        for _ in range(self.rows * self.cols):
            cell = Label(
                text='',
                background_color=CINZA,
                size_hint=(1, 1)
            )
            self.cells.append(cell)
            self.add_widget(cell)

class TermooApp(App):
    def build(self):
        self.game = TermooGame()
        self.n_letras = 5
        self.palavra_atual = self.escolher_palavra()
        self.tentativa_atual = 0
        
        # Layout principal
        layout = TermooLayout()
        
        # Título
        layout.add_widget(Label(
            text='TERMOO',
            size_hint_y=None,
            height=50
        ))
        
        # Grid do jogo
        self.grid = LetterGrid(self.n_letras)
        layout.add_widget(self.grid)
        
        # Campo de entrada
        self.entrada = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            on_text_validate=self.verificar_palavra
        )
        layout.add_widget(self.entrada)
        
        # Teclado virtual
        self.criar_teclado(layout)
        
        return layout
    
    def criar_teclado(self, layout):
        teclado = GridLayout(
            cols=10,
            spacing=2,
            size_hint_y=None,
            height=200
        )
        
        letras = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        for letra in letras:
            btn = Button(
                text=letra,
                on_press=self.press_key,
                background_normal='',
                background_color=CINZA
            )
            teclado.add_widget(btn)
            
        layout.add_widget(teclado)
    
    def escolher_palavra(self):
        palavras_validas = [p for p in self.game.palavras_possiveis if len(p) == self.n_letras]
        palavra = random.choice(palavras_validas)
        return self.game.remover_acentos(palavra.lower())
    
    def press_key(self, instance):
        self.entrada.text += instance.text.lower()
    
    def verificar_palavra(self, instance):
        chute = self.entrada.text.lower()
        
        if len(chute) != self.n_letras:
            self.mostrar_erro(f"Use {self.n_letras} letras!")
            return
            
        resultado = self.game.verifica_palavra(chute, self.palavra_atual)
        self.atualizar_grid(chute, resultado)
        self.entrada.text = ''
        self.tentativa_atual += 1
        
        if all(r == 'verde' for r in resultado):
            self.mostrar_vitoria()
        elif self.tentativa_atual >= 6:
            self.mostrar_derrota()
    
    def atualizar_grid(self, chute, resultado):
        for i, (letra, cor) in enumerate(zip(chute, resultado)):
            cell = self.grid.cells[self.tentativa_atual * self.n_letras + i]
            cell.text = letra.upper()
            if cor == 'verde':
                cell.background_color = VERDE
            elif cor == 'amarelo':
                cell.background_color = AMARELO
            else:
                cell.background_color = CINZA
    
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
            content=Label(text='Você acertou!'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
    
    def mostrar_derrota(self):
        popup = Popup(
            title='Fim de Jogo',
            content=Label(text=f'A palavra era: {self.palavra_atual.upper()}'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    Window.clearcolor = (0.9, 0.9, 0.9, 1)
    TermooApp().run()
