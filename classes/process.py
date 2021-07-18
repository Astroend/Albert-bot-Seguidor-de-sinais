# Processo para seguir os sinais, recebendo as variáveis e executando as ordens.

from iqoptionapi.stable_api import IQ_Option
from datetime import datetime


class Process():
    def __init__(self, email, password , account_type,value, martingale, sinais, option, stop_win, stop_loss, multiplicador):
        self.__email = email # E-mail de acesso da IqOption.
        self.__password = password # Senha de acesso da IqOption.
        self.__value = value # Valor das operações.
        self.__martingale = martingale + 1# Número de martingales.
        self.__sinais = sinais # Lista de sinais em formato de dicionário.
        self.__option = option.upper() # Preferência de entrada ( binária ou digital ).
        self.__stop_win = stop_win # Parâmetro de máximo de ganhos.
        self.__stop_loss = stop_loss # Parâmetro de máximo de percas.
        self.__multiplicador = multiplicador # Parâmetro de multiplicação do martingale.
        self.__account_type = account_type.upper() # Define o tipo de conta ( REAL OU PRACTICE )
        self.connect()
        self.__banca = self.API.get_balance()
        self.operate()

    # Realiza a conexão do websocket à Iq Option.
    def connect(self):
        self.API = IQ_Option(self.__email, self.__password)
        self.API.connect() # Realiza a conexão
        self.API.change_balance(self.__account_type)

    # Aguarda o momento correto para realizar a entrada.
    def its_time(self, hour):
        now = datetime.now()
        #print(hour)
        date = datetime(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), int(hour[0]), int(hour[1]), 00)
        print("Aguardando o horário de compra")
        while True:
            #print(date ,datetime.timestamp(date), self.API.get_server_timestamp())
            if (datetime.timestamp(date)-2) >= self.API.get_server_timestamp() and datetime.timestamp(date) <= (self.API.get_server_timestamp()+5):
                return True
            if (datetime.timestamp(date)+10) < self.API.get_server_timestamp():
                print("Horário de compra passou.")
                return False

    # Parâmetros de parada do automatizador.
    def stop(self):
        if self.API.get_balance() >= (self.__banca + self.__stop_win):
            print("Stop win batido.")
            input("Pressione enter para sair.")
            exit()
        if self.API.get_balance() <= (self.__banca - self.__stop_loss):
            print("Stop loss batido.")
            input("Pressione enter para sair.")
            exit()
        if self.API.get_balance() < (self.__banca + self.__stop_win) and self.API.get_balance() > (self.__banca - self.__stop_loss): return True
  
    # Abre as ordens em opções binárias.
    def buy_binary(self, active, action, duration, time):
        value = self.__value
        for trie in range(self.__martingale):
            check,id=self.API.buy(value, active, action, duration)
            if check:
                if value > self.__value: print(f"{trie}ª Martingale")
                print(f"Ordem de {action} em {active} de {value} aberta.")
            else:
                print(f"Oops, tive um problema em abrir a ordem {active} as {time}")
                return 0
            result = self.API.check_win_v3(id)
            if result < 0: value*= self.__multiplicador
            print(f"Resultado da ordem {result}")
            if result > 0: return result

    # Abre as ordens em opções digital.
    def buy_digital(self, active, action, duration, time):
        value = self.__value
        for trie in range(self.__martingale):
            _, id = self.API.buy_digital_spot(active, value, action.lower(), duration)
            if id !="error":
                if value > self.__value : print(f"{trie}ª Martingale")
                print(f"Ordem de {action} em {active} de {value} aberta.")
                while True:
                    check,win=self.API.check_win_digital_v2(id)
                    if check==True:
                        break
                if win<0:
                    print(f"Resultado da ordem -R${win}")
                    value *= self.__multiplicador
                if win > 0:
                    print(f"Resultado da ordem +R${win}")
                    return win
            else:
                print(f"Oops, tive um problema em abrir a ordem {active} as {time}")

    # Inicia as operações.
    def operate(self):
        for item in self.__sinais:
            if self.stop():
                entrar = self.its_time(item['Hour'])
                if entrar == True:
                    if self.__option == "BINARY":
                        self.buy_binary(item["Active"], item["Action"], item["Duration"], item["Hour"])
                    else:    
                        self.buy_digital(item["Active"], item["Action"], item["Duration"], item["Hour"])
                else: continue