from classes.layouts import Layouts
import gif_image.gif

from datetime import datetime
import os


class Action_functions():
    
    def open_link():
        os.system('start www.astroend.xyz/termos.html')

    def gif():
        window = Layouts.window_loading()

        while True:
            event = window.Read(timeout=25)
            window.Element('_IMAGE_').UpdateAnimation(gif_image.gif.gif,  time_between_frames=50)

# Classe referente ao sinal atual / proximo sinal
class Actual_signal():
    # Lista de sinais é requerida (em dict) * .convert *
    def __init__(self, sinais):
        self.__sinais = sinais

    # Retorna uma string referente ao próximo sinal.
    def get_next(self):
        now = datetime.now()
        for signal in self.__sinais:
            try:
                if signal["Duration"].count("M") or signal["Duration"].count("H"):
                    signal["Duration"] = self.convert_time(signal["Duration"])
                else: pass
            except: pass
            try: signal_hour = (datetime(int(now.strftime("%Y")), int(signal["Date"][1]), int(signal["Date"][0]), int(signal["Hour"][0]), int(signal["Hour"][1]))).timestamp()
            except: signal_hour = (datetime(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), int(signal["Hour"][0]), int(signal["Hour"][1]))).timestamp()
            if now.timestamp() >= signal_hour: continue
            else:
                if signal["Duration"] < 60:
                    signal["Duration"] = f"M{signal['Duration']}"
                else: signal["Duration"] = f"H{(signal['Duration'])/60}"
                return f'''{signal["Duration"]}-{signal["Active"]}-{signal["Hour"][0]}:{signal["Hour"][1]}-{signal["Action"]}'''

    def convert_time(self, time):
        multiplier = time[0:1]
        if multiplier.upper() == "H":
            return int(time[1:]*60)
        else: 
            return int(time[1:])

class Where_save():
    ''' Classe de manipulação do TXT que armazena o caminho do diretório '''

    def find(self):
        '''Busca o directory.txt'''
        try:
            with open('Directory.txt', 'r', encoding='UTF-8') as file:
                '''Retorna True e o conteúdo do arquivo txt'''
                return (True, file.read())
        except:
            '''Retorna False e uma string caso o txt não exista'''
            return (False, "Arquivo não existente.")

    def create(self, string):
        '''Cria o arquivo txt e escreve o caminho do diretório.'''
        with open('Directory.txt', 'w', encoding='UTF-8') as file:
            try: 
                file.write(string)
                '''Retorna True caso tenha sido bem sucedido.'''
                return True
            except: 
                '''Retorna False e uma mensagem caso não seja bem sucedido.'''
                return (False, "Erro em criar o diretório")