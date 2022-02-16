
from classes.layouts import Layouts
import gif_image.gif

from datetime import datetime
from gettext import find
import os


class Action_functions():
    
    def open_link():
        os.system('start www.astroend.xyz/termos.html')

    def gif():
        window = Layouts.window_loading()

        while True:
            event = window.Read(timeout=25)
            window.Element('_IMAGE_').UpdateAnimation(gif_image.gif.gif,  time_between_frames=50)

'''Classe referente ao sinal atual / proximo sinal'''
class Actual_signal():
    '''Lista de sinais é requerida (em dict) * .convert *'''
    def __init__(self, sinais):
        self.__sinais = sinais

    '''Retorna uma string referente ao próximo sinal.'''
    def get_next(self):
        now = datetime.now()
        for signal in self.__sinais:
            # try:
            #     if signal["Duration"].count("M") or signal["Duration"].count("H"):
            #         signal["Duration"] = self.convert_time(signal["Duration"])
            #     else: pass
            # except: pass
            try: signal_hour = (datetime(int(now.strftime("%Y")), int(signal["Date"][1]), int(signal["Date"][0]), int(signal["Hour"][0]), int(signal["Hour"][1]))).timestamp()
            except: signal_hour = (datetime(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), int(signal["Hour"][0]), int(signal["Hour"][1]))).timestamp()
            if now.timestamp() >= signal_hour: continue
            else:
                if signal["Duration"] < 60:
                    duration = f"M{signal['Duration']}"
                else: duration = f"H{(signal['Duration'])/60}"
                return f'''{duration}-{signal["Active"]}-{signal["Hour"][0]}:{signal["Hour"][1]}-{signal["Action"]}'''

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

class Write_txt():
    '''Escreve os valores no arquivo TXT'''
  
    '''Declara as variáveis month_names e month para uso posterior'''
    def __init__(self):
        self.month_names = [None, 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        self.month = self.month_names[int(datetime.now().strftime('%m'))]
        self.today = datetime.now()
        self.file_path = Where_save().find()

    '''Verifica a existência do diretório / cria o diretório'''
    def directory(self):
        if os.path.exists(f'''{self.file_path}/{self.month}'''):
            '''Se o diretório já existir.'''
            self.file_path = f'''{self.file_path}/{self.month}'''
            print(self.file_path)
            return (True, 'Diretório já existente')
        else: 
            '''Se o diretório não existir ele cria o diretório'''
            os.makedirs(f'''{self.file_path}/{self.month}''')
            self.file_path = f'''{self.file_path}/{self.month}'''
            print(self.file_path)

            return (True, 'Diretório criado')

    '''Escreve / cria arquivo txt no diretório especificado.'''
    def write(self, txt):
        files = self.file_path[1]
        if os.path.exists(f'''{files}/{datetime.now().strftime('%d-%m-%Y')}.txt'''):
            '''Se arquivo txt existe.'''
            with open(f'''{files}/{datetime.now().strftime('%d-%m-%Y')}.txt''', 'r') as file:
                '''Abre o arquivo em modo de leitura.'''
                if (file.read()[len(file.read())-2:]) == '\n':
                    '''Verifica se o último valor é uma quebra de linha.'''
                    with open(f'''{files}/{datetime.now().strftime('%d-%m-%Y')}.txt''', 'a') as text:
                        '''Abre novamente o arquivo mas em modo de adicionar texto.'''
                        text.write(txt) # Escreve no arquivo txt.        
                else:
                    '''Se não for, ele inicia a linha com uma quebra de linha.'''
                    with open(f'''{files}/{datetime.now().strftime('%d-%m-%Y')}.txt''', 'a') as text:
                        text.write('\n' + txt) # Escreve no arquivo txt.          
        else:
            '''Se não existe, arquivo txt é criado.'''
            with open(f'''{files}/{datetime.now().strftime('%d-%m-%Y')}.txt''', 'a') as file:
                '''Abre o arquivo em modo de adicionar text'''
                file.write(txt) # Escreve no arquivo txt.

if __name__ == '__main__':
    save = Where_save().find()
    print(save)
    salve = Write_txt().write("boa noite")
    