# Classe de acesso direto ás informações de usuário.
from iqoptionapi.stable_api import IQ_Option

from classes.readTXT import Read

from datetime import datetime

class Api():

    # Variável de controle de uso do bot.
    def check(self, boolean):
        self.check = boolean # True = operando, False = não operando
    
    # Define o parâmetro de limite de ganhos do usuário.
    def stop_win(self, num):
        self.stop_win = num # Ganho esperado
        self.stop_win_complete = self.API.get_balance() + num # Valor da banca esperada.

    # Define o parâmetro de limite de perca do usuário.   
    def stop_loss(self, num):
        self.stop_loss = num # Perda máxima
        self.stop_loss_complete = self.API.get_balance() - num # Valor da banca de perca esperada.
    
    # Define o valor das entradas.
    def value(self, num):
        self.value = num
        
    # Define o número de martingales
    def martingale(self, num):
        self.martingale = num
    
    # Define a preferência entre binária ou digital.
    def option(self, type):
        self.option = type
    
    def sinais(self, dict):
        self.sinais = dict # Sinais em dicionário.

    def multiplicador(self, float):
        self.multiplicador = float
    # Retorna os sinais em dicionário.
    @property
    def get_sinais(self):
        return self.sinais

    # Retorna opções abertas de outros computadores.
    @property
    def get_options(self):
        return self.API.get_option_open_by_other_pc()
    
    # Retorna valor do stop loss completo.
    @property
    def get_stop_loss_complete(self):
        #stop loss + banca (stop = 10 + banca = 100: retorna 90)
        return self.stop_loss_complete

    # Retorna valor do stop win completo.
    @property    
    def get_stop_win_complete(self):
        #stop win + banca (win = 10 + banca = 100: retorna 110)
        return self.stop_win_complete
        
    # Retorna o Objeto API para uso interno.
    @property
    def get_api(self):
        return self.API
    
    # Retorna o valor do stop win.
    @property
    def get_stop_win(self):
        #retorna valor do stop win (win = 10 : retorna 10)
        return self.stop_win

    # Retorna o valor do stop loss. 
    @property
    def get_stop_loss(self):
        #retorna valor do stop loss (loss = 10 : retorna 10)
        return self.stop_loss
        
    # Retorna o valor das entradas.
    @property
    def get_value(self):
        return self.value
    
    # Retorna a quantidade de martingales.
    @property
    def get_martingale(self):
        return self.martingale
    
    # Retorna a preferência de usuário.
    @property
    def get_option(self):
        return self.option
    
    # Retorna o horário do servidor em segundos.
    @property
    def get_time(self):
        return self.API.get_server_timestamp()

    # Retorna a data do servidor em dd/mm/aaaa
    @property
    def get_date(self):
        return datetime.fromtimestamp(self.API.get_server_timestamp())

    # Retorna o multiplicador
    @property
    def get_multiplicador(self):
        return self.multiplicador

    # Retorna o email do usuário.
    @property
    def get_email(self):
        return self.email
    # Retorna o email do usuário.
    @property
    def get_password(self):
        return self.password

    def connect(self, email, senha):
        self.__email(email)
        self.__password(senha)
        self.API = IQ_Option(email, senha)
        status, message = self.API.connect()
        return status
    
    def type(self, balance):
        self.account_type = balance
        if balance.upper() != 'REAL' or balance.upper() != 'PRACTICE':
            return f'{balance} é inválido.' 
        return self.API.change_balance(balance.upper())
    
    # Define o email de acesso do usuário.    
    def __email(self, string):
        self.email = string 
    
    # Define a senha de acesso do usuário.
    def __password(self, string):
        self.password = string
        
    @property
    def get_type(self):
        return self.account_type
    
    @property    
    def get_connected(self):
        return self.API.check_connect()
    
    @property
    def get_balance(self):
        return self.API.get_balance()