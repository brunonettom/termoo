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
from listaDePalavrasFinal_01_12_2024__22_28 import palavras  # Importando sua lista de palavras
import random
import unicodedata

# Cores do jogo
VERDE = get_color_from_hex('#32CD32')
AMARELO = get_color_from_hex('#FFD700')
CINZA = get_color_from_hex('#808080')
BRANCO = get_color_from_hex('#FFFFFF')

class TermooGame:
    def __init__(self):
        self.palavras_disponiveis = [palavra.lower() for palavra in palavras if ' ' not in palavra and '-' not in palavra]
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
        
        # Primeiro verifica as letras verdes
        for i in range(len(chute)):
            if chute[i] == palavra_chave[i]:
                resultado[i] = 'verde'
                palavra_temp[i] = None
        
        # Depois verifica as amarelas
        for i in range(len(chute)):
            if resultado[i] == 'cinza' and chute[i] in palavra_temp:
                resultado[i] = 'amarelo'
                palavra_temp[palavra_temp.index(chute[i])] = None
                
        return resultado

class ConfigPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.title = 'Configurações do Jogo'
        self.size_hint = (0.8, 0.6)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input para número de letras
        letras_layout = BoxLayout()
        letras_layout.add_widget(Label(text='Número de letras:'))
        self.letras_input = TextInput(text='5', multiline=False, input_filter='int')
        letras_layout.add_widget(self.letras_input)
        layout.add_widget(letras_layout)
        
        # Input para número de palavras
        palavras_layout = BoxLayout()
        palavras_layout.add_widget(Label(text='Número de palavras:'))
        self.palavras_input = TextInput(text='2', multiline=False, input_filter='int')
        palavras_layout.add_widget(self.palavras_input)
        layout.add_widget(palavras_layout)
        
        # Botão de confirmação
        confirmar = Button(text='Começar Jogo', size_hint_y=None, height=50)
        confirmar.bind(on_press=self.confirmar_config)
        layout.add_widget(confirmar)
        
        self.content = layout
    
    def confirmar_config(self, instance):
        n_letras = int(self.letras_input.text)
        n_palavras = int(self.palavras_input.text)
        self.callback(n_letras, n_palavras)
        self.dismiss()

class TermooGrid(GridLayout):
    def __init__(self, n_letras, n_palavras, **kwargs):
        super().__init__(**kwargs)
        self.cols = n_letras
        self.rows = 6  # Número de tentativas
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
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Mostrar popup de configuração ao iniciar
        config_popup = ConfigPopup(self.iniciar_jogo)
        config_popup.open()
        
        return self.layout
    
    def iniciar_jogo(self, n_letras, n_palavras):
        self.n_letras = n_letras
        self.n_palavras = n_palavras
        self.palavras_chave = self.escolher_palavras()
        self.palavra_atual_index = 0
        
        # Limpa o layout anterior
        self.layout.clear_widgets()
        
        # Grid do jogo
        self.grid = TermooGrid(n_letras=n_letras, n_palavras=n_palavras)
        self.layout.add_widget(self.grid)
        
        # Campo de entrada
        self.entrada = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            on_text_validate=self.verificar_palavra
        )
        self.layout.add_widget(self.entrada)
        
        # Teclado
        self.teclado = TermooTeclado(self.press_key)
        self.layout.add_widget(self.teclado)
    
    def escolher_palavras(self):
        palavras_validas = [p for p in self.game.palavras_disponiveis if len(p) == self.n_letras]
        return random.sample(palavras_validas, self.n_palavras)
    
    def press_key(self, instance):
        self.entrada.text += instance.text.lower()
    
    def verificar_palavra(self, instance):
        chute = self.entrada.text.lower()
        if len(chute) != self.n_letras:
            self.mostrar_erro(f"A palavra deve ter {self.n_letras} letras!")
            return
        
        if chute not in self.game.palavras_disponiveis:
            self.mostrar_erro("Palavra não encontrada na lista!")
            return
        
        palavra_chave_atual = self.palavras_chave[self.palavra_atual_index]
        resultado = self.game.verifica_palavra(chute, palavra_chave_atual)
        self.atualizar_grid(chute, resultado)
        self.entrada.text = ''
        
        if all(r == 'verde' for r in resultado):
            self.palavra_atual_index += 1
            if self.palavra_atual_index >= len(self.palavras_chave):
                self.mostrar_vitoria()
            else:
                self.mostrar_proxima_palavra()
    
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
            content=Label(text='Você completou todas as palavras!'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
    
    def mostrar_proxima_palavra(self):
        popup = Popup(
            title='Muito bem!',
            content=Label(text=f'Próxima palavra! ({self.palavra_atual_index + 1}/{len(self.palavras_chave)})'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    Window.clearcolor = (0.9, 0.9, 0.9, 1)
    TermooApp().run()