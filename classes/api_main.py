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
        return self.banca

    def update_balance(self):
        self.banca = self.API.get_balance()

    def set_status(self):
        self.status = not self.status

    @property
    def get_status(self):
        return self.status

    # Aguarda o momento correto para realizar a entrada.
    def its_time(self, hour):
        now = datetime.now()
        #print(hour)
        date = datetime(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), int(hour[0]), int(hour[1]), 00)
        print("Aguardando o horário de compra")
        while True:
            if not self.stop(): break
            #print(date ,datetime.timestamp(date), self.API.get_server_timestamp())
            timestamp_ = self.API.get_server_timestamp() 

            if (datetime.timestamp(date)-2) <= timestamp_ and datetime.timestamp(date) <= (timestamp_+5):
                return True
            if (datetime.timestamp(date)+10) < self.API.get_server_timestamp():
                print("Horário de compra passou.")
                return False

    # Parâmetros de parada do automatizador.
    def stop(self):
        if self.status == True:
            return False
        if self.API.get_balance() >= (self.banca + self.stop_win):
            print("Stop win batido.")
            input("Pressione enter para sair.")
            return False
        if self.API.get_balance() <= (self.banca - self.stop_loss):
            print("Stop loss batido.")
            input("Pressione enter para sair.")
            return False
        if self.API.get_balance() < (self.banca + self.stop_win) and self.API.get_balance() > (self.banca - self.stop_loss): return True
  
    # Abre as ordens em opções binárias.
    def buy_binary(self, active, action, duration, time):
        value = self.value
        for trie in range(self.martingale + 1):
            check,id=self.API.buy(value, active, action, duration)
            if check:
                if value > self.__value: print(f"{trie}ª Martingale")
                print(f"Ordem de {action} em {active} de {value} aberta.")
            else:
                print(f"Oops, tive um problema em abrir a ordem {active} as {time}")
                return 0
            result = self.API.check_win_v3(id)
            if result < 0: 
                if trie == self.martingale-1:
                    self.txt.write(f'''R$ {result} - {active} - {time} - {action}''')
                value*= self.multiplicador
            print(f"Resultado da ordem {result}")
            if result > 0: 
                self.txt.write(f'''R$ +{result} - {active} - {time} - {action}''')
                return result

    # Abre as ordens em opções digital.
    def buy_digital(self, active, action, duration, time):
        value = self.value
        for trie in range(self.martingale +1):
            _, id = self.API.buy_digital_spot(active, value, action.lower(), duration)
            if id !="error":
                if value > self.value : print(f"{trie}ª Martingale")
                print(f"Ordem de {action} em {active} de {value} aberta.")
                while True:
                    check,win=self.API.check_win_digital_v2(id)
                    if check==True:
                        break
                if win<0:
                    print(f"Resultado da ordem -R${win}")
                    value *= self.multiplicador
                    if trie == self.martingale-1:
                        self.txt.write(f'''R$ -{win} - {active} - {time} - {action}''')
                if win > 0:
                    print(f"Resultado da ordem +R${win}")

                    self.txt.write(f'''R$ +{win} - {active} - {time} - {action}''')
                    return win
            else:
                print(f"Oops, tive um problema em abrir a ordem {active} as {time}")

    # Inicia as operações.
    def operate(self):
        self.status = False
        for item in self.sinais:
            if self.stop():
                entrar = self.its_time(item['Hour'])
                if entrar == True:
                    if self.option == "BINARY":
                        self.buy_binary(item["Active"], item["Action"], item["Duration"], item["Hour"])
                    else:    
                        self.buy_digital(item["Active"], item["Action"], item["Duration"], item["Hour"])
                else: continue

        print("acabou")