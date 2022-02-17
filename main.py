from PySimpleGUI import PySimpleGUI as sg
from multiprocessing import Process, Manager, freeze_support
from threading import Thread
import logging
import os

from classes.action_functions import Action_functions, Actual_signal, Where_save
from classes.layouts import Layouts
from classes.readTXT import Read
from classes.api_main import Api

class Main():

    def __init__(self):
        os.system("cls")
        logging.info("****START****\n\n")
        operate = False
        api = Api()
        window_astroend, window_file, window_login, pop_up, window_option, window_trading, window_terminate = Layouts.window_astroend(
        ), None, None, None, None, None, None

        status, message = Where_save().find()


        if status:
            file_historic = message
            logging.info(" -- CAMINHO SALVO: '" +file_historic+"'\n")
        else:
            logging.info(" -- CAMINHO NÃO ENCONTRADO\n")

        while True:

            window, event, values = sg.read_all_windows(timeout=25)

            if window == window_astroend and event == sg.WIN_CLOSED:
                logging.info("\n****EXIT****\n")
                break

            if window == window_astroend and event == 'TERMOS':
                link = Process(target=Action_functions.open_link)
                link.start()
                logging.info(" -- TERMOS \n")

            if window == window_astroend and event == 'ACEITO OS TERMOS':
                logging.info(" -- TERMOS ACEITOS\n")
                window_astroend.close()

                if status:
                    logging.info(" -- WINDOW LOGIN\n")
                    window_login = Layouts.window_login()
                else:
                    logging.info(" -- WINDOW FILE\n")
                    window_file = Layouts.window_file()

            if window == window_file and event == sg.WIN_CLOSED:
                logging.info("\n****EXIT****\n")
                break

            if window == window_file and event == 'Enviar':
                logging.info(" -- CAMINHO ENVIADO: '" +values['file']+ "'\n")
                window_file['file_historic'].update(values['file'])

            if window == window_file and event == 'Escolher':
                Where_save().create(values['file'])

                status, message = Where_save().find()
                if status:
                    logging.info(" -- CAMINHO SALVO\n")
                    file_historic = message

                window_file.close()
                logging.info(" -- WINDOW LOGIN\n")
                window_login = Layouts.window_login()

            if window == window_login and event == sg.WIN_CLOSED:
                logging.info("\n****EXIT****\n")
                break

            if window == window_login and event == 'Entrar':

                password = ('*' * len(values['password']))
                
                logging.info(" -- LOGIN: {'" + values['login'] + "', '" + password +"'}\n")
                window_login.close()

                loading = Process(target=Action_functions.gif)
                loading.start()

                if(api.connect(values['login'], values['password'])):
                    logging.info(" -- CONECTADO \n")
                    api.update_balance()
                    loading.terminate()
                    window_option = Layouts.window_option()
                else:
                    loading.terminate()
                    logging.info(" -- ERRO AO CONECTAR\n")
                    pop_up = Layouts.pop_up()
                    window_login = Layouts.window_login()

            if window == window_option and event == sg.WIN_CLOSED:
                logging.info("\n****EXIT****\n")
                break

            if window == window_option and event == 'Enviar':
                window_option['listbox'].update(Read(values['file']).to_list())
                file = Read(values['file']).convert()
                logging.info(" -- SINAIS ENVIADOS\n")
                api.sinais(file)

            if window == window_option and event == 'Operar':

                api.type('PRACTICE' if values['account_practice'] else 'REAL')
                api.option('BINARY' if values['option_binary'] else 'DIGITAL')
                api.value(float(((str(values['value'])).replace(',', '.'))))
                api.stop_win(
                    float(((str(values['stop_win'])).replace(',', '.'))))
                api.stop_loss(
                    float((str(values['stop_loss'])).replace(',', '.')))
                api.martingale(int(values['martingale']))
                api.multiplicador(
                    float((str(values['multiplier'])).replace(',', '.')))
                api.file(file)

                logging.info(" -- COMEÇANDO: {'"+str(api.get_type)+"', '"+str(api.get_balance)+"', '"+str(api.get_martingale)+"', '"
                    +str(api.get_stop_win_complete)+"', '"+str(api.get_stop_loss_complete)+"', '"
                    +str(api.get_option)+"', '"+str(api.get_multiplicador)+"', '"+str(api.get_value)+"'}\n")

                trading_ = Thread(target=api.operate)

                trading_.start()

                window_option.close()
                operate = True
                window_trading = Layouts.window_trading(
                    api.get_type, api.get_balance, api.get_martingale, api.get_stop_win_complete, api.get_stop_loss_complete)

            if window == window_trading and event == sg.WIN_CLOSED:
                api.set_status()
                operate = False
                break

            if operate:
                sinal = (f"{Actual_signal(file).get_next()}")
                window_trading['-balance-'].update(f"Banca: {api.get_balance}")
                window_trading['-status-'].update('Meta batida' if api.get_balance >= api.get_stop_win_complete else 'Stop atingido' if api.get_balance <=
                                                  api.get_stop_loss_complete else f'Trabalhando ...' if api.get_balance > 0 else 'Sem fundos')
                window_trading['-signal-'].update(sinal if (sinal != "None") else "Sem Sinais")

            if window == window_trading and event == 'Finalizar':
                api.set_status()
                operate = False

                window_trading.close()
                window_terminate = Layouts.window_finalize(api.get_balance, file_historic)

            if window == window_terminate and event == sg.WIN_CLOSED:
                logging.info("\n****EXIT****\n")
                break

            if window == window_terminate and event == 'Fechar':
                logging.info("\n****EXIT****\n")
                break


if __name__ == '__main__':
    freeze_support()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',filename='app.log',filemode='w')
    Main()
