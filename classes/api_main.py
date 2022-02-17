# Classe de acesso direto ás informações de usuário.
from iqoptionapi.stable_api import IQ_Option

from classes.readTXT import Read
from classes.action_functions import Write_txt

from datetime import datetime
import logging
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

    def file(self, file):
        self.txt = Write_txt(file)
        self.txt.directory()

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
        date = datetime(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), int(hour[0]), int(hour[1]), 00)
        while True:
            if not self.stop(): break
            #print(date ,datetime.timestamp(date), self.API.get_server_timestamp())
            timestamp_ = self.API.get_server_timestamp()

            logging.info(f"  ## [{datetime.now().strftime('%H:%M:%S')}] :: Aguardando... ("+str(date)+")", end='\r')

            if (datetime.timestamp(date)-2) <= timestamp_ and datetime.timestamp(date)+1 >= timestamp_:
                logging.info(f"\r  ## [{datetime.now().strftime('%H:%M:%S')}] :: Comprando...                          ")
                return True
            if (datetime.timestamp(date)+10) < timestamp_:
                logging.info(f"  ## [{datetime.now().strftime('%H:%M:%S')}] :: Aguardando... ("+str(date)+")", end='\r')
                return False

    # Parâmetros de parada do automatizador.
    def stop(self):
        if self.status == True:
            return False
        if self.API.get_balance() >= (self.banca + self.stop_win):
            logging.info("  ## Stop win batido.\n")
            txt = (f'''   ##### STOP WIN #####''')
            Write_txt().write(txt)
            return False
        if self.API.get_balance() <= (self.banca - self.stop_loss):
            logging.info(" ## Stop loss batido.\n")
            txt = (f'''   ##### STOP LOSS #####''')
            Write_txt().write(txt)
            return False
        if self.API.get_balance() < (self.banca + self.stop_win) and self.API.get_balance() > (self.banca - self.stop_loss): return True
  
    # Abre as ordens em opções binárias.
    def buy_binary(self, active, action, duration, time):
        value = self.value
        for trie in range(self.martingale + 1):
            check,id=self.API.buy(value, active, action, duration)
            if check:
                if trie != 0: print(f"  ## {trie}ª Martingale")
                logging.info(f"  ## Ordem de {action} em {active} de {value} aberta.")
            else:
                logging.info(f"  ## Oops, tive um problema em abrir a ordem {active} as {time}\n")
                txt = (f''' ## Problemas em {active} as {time}''')
                Write_txt().write(txt)
                return 0
            result = self.API.check_win_v3(id)
    
            value*= self.multiplicador
            saldo = round(float(result),2)
            if (trie == 0):
                txt = (f'''{duration} / {active} / {action} / {time} / {self.get_type} / {self.get_option} / $ {saldo}''')
            else:
                txt = (f'''{duration} / {active} / {action} / {time} / {self.get_type} / {self.get_option} / $ {saldo} / Martingale {trie}''')
            Write_txt().write(txt)
            logging.info(f"  ## Resultado da ordem {result}")
            logging.info("  ## Operação Salva \n")

    # Abre as ordens em opções digital.
    def buy_digital(self, active, action, duration, time):
        value = self.value
        for trie in range(self.martingale + 1):
            _, id = self.API.buy_digital_spot(active, value, action.lower(), duration)
            if id !="error":
                if (trie != 0) : print(f"  ## {trie}ª Martingale")
                logging.info(f"  ## Ordem de {action} em {active} de {value} aberta.")
                while True:
                    check,win=self.API.check_win_digital_v2(id)
                    if check==True:
                        break
  
                logging.info(f"  ## Resultado da ordem -R${win}")
                value *= self.multiplicador
                if trie == self.martingale:
                    #txt = (f'''R$ -{win} - {active} - {time} - {action}''')
                    saldo = round(float(win),2)
                    if (trie == 0):
                        txt = (f'''{duration} / {active} / {action} / {time} / {self.get_type} / {self.get_option} / $ {saldo}''')
                    else:
                        txt = (f'''{duration} / {active} / {action} / {time} / {self.get_type} / {self.get_option} / $ {saldo} / Martingale {trie}''')
                    Write_txt().write(txt)
                    logging.info("  ## Operação Salva \n")
                 
            else:
                logging.info(f"  ## Oops, tive um problema em abrir a ordem {active} as {time}\n")
                txt = (f''' ## Problemas em {active} as {time}''')
                Write_txt().write(txt)
                logging.info("  ## Operação Salva \n")

    # Inicia as operações.
    def operate(self):
        self.status = False
        logging.info("  ## TRABALHANDO...\n")
        txt = (f''' --- COMECO --- ''')
        Write_txt().write(txt)
        for item in self.sinais:
            if self.stop():
                entrar = self.its_time(item['Hour'])
                if entrar == True:
                    if self.option == "BINARY":
                        self.buy_binary(item["Active"], item["Action"], item["Duration"], item["Hour"])
                    else:    
                        self.buy_digital(item["Active"], item["Action"], item["Duration"], item["Hour"])
                else: continue

        logging.info("\n\n  ## ...FINALIZADO\n")
        txt = (f''' --- FIM --- ''')
        Write_txt().write(txt)
