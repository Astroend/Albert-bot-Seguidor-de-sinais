from PySimpleGUI import PySimpleGUI as sg
from multiprocessing import Process, Manager, freeze_support
from threading import Thread

from classes.action_functions import Action_functions, Actual_signal, Where_save
from classes.layouts import Layouts
from classes.readTXT import Read
from classes.api_main import Api


class Main():

    def __init__(self):

        operate = False
        api = Api()
        window_astroend, window_file, window_login, pop_up, window_option, window_trading, window_terminate = Layouts.window_astroend(
        ), None, None, None, None, None, None

        status, message = Where_save().find()

        if status:
            file_historic = message

        while True:

            window, event, values = sg.read_all_windows(timeout=25)

            if window == window_astroend and event == sg.WIN_CLOSED:
                break

            if window == window_astroend and event == 'TERMOS':
                link = Process(target=Action_functions.open_link)
                link.start()

            if window == window_astroend and event == 'ACEITO OS TERMOS':
                window_astroend.close()

                if status:
                    window_login = Layouts.window_login()
                else:
                    window_file = Layouts.window_file()

            if window == window_file and event == sg.WIN_CLOSED:
                break

            if window == window_file and event == 'Enviar':
                window_file['file_historic'].update(values['file'])

            if window == window_file and event == 'Escolher':
                Where_save().create(values['file'])

                status, message = Where_save().find()
                if status:
                    file_historic = message

                window_file.close()
                window_login = Layouts.window_login()

            if window == window_login and event == sg.WIN_CLOSED:
                break

            if window == window_login and event == 'Entrar':

                window_login.close()

                loading = Process(target=Action_functions.gif)
                loading.start()

                if(api.connect(values['login'], values['password'])):
                    api.update_balance()
                    loading.terminate()
                    window_option = Layouts.window_option()
                else:
                    loading.terminate()
                    pop_up = Layouts.pop_up()
                    window_login = Layouts.window_login()

            if window == window_option and event == sg.WIN_CLOSED:
                break

            if window == window_option and event == 'Enviar':
                window_option['listbox'].update(Read(values['file']).to_list())
                file = Read(values['file']).convert()
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
                window_trading['-balance-'].update(f"Banca: {api.get_balance}")
                window_trading['-status-'].update('Meta batida' if api.get_balance >= api.get_stop_win_complete else 'Stop atingido' if api.get_balance <=
                                                  api.get_stop_loss_complete else f'Trabalhando ...' if api.get_balance > 0 else 'Sem fundos.')
                window_trading['-signal-'].update(
                    f"{Actual_signal(file).get_next()}")

            if window == window_trading and event == 'Finalizar':
                api.set_status()
                operate = False

                window_trading.close()
                window_terminate = Layouts.window_finalize(api.get_balance)

            if window == window_terminate and event == sg.WIN_CLOSED:
                break

            if window == window_terminate and event == 'Fechar':
                break


if __name__ == '__main__':
    freeze_support()
    Main()
