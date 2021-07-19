from PySimpleGUI import PySimpleGUI as sg

import gif_image.gif

class Layouts():

    def window_astroend():
        sg.theme('DarkBlack1')
        layout_column = [
            [sg.Text('ALBERT BOT - SINAIS', size=(20,1), font='ANY 20', justification='center')],
            [sg.Text('por ASTROEND', size=(46,1), font='ANY 8', justification='right')],
            [sg.Text('')],
            [sg.Button('TERMOS') ,sg.Button('ACEITO OS TERMOS')]
        ]   
        layout = [[sg.Column(layout_column, element_justification='center')]]
        return sg.Window('Astroend - v0.1', layout=layout, finalize=True, size=(350,160),margins=(20,15,20,20))

    def window_login():
        sg.theme('DarkBlack1')
        layout_column = [
            [sg.Text('Login: ', size=(5,1), font='ANY 11'), sg.Input(key='login', size=(20,2))],
            [sg.Text('Senha: ', size=(5,1), font='ANY 11'), sg.Input(key='password', size=(20,2), password_char='*')],
            [sg.Text('')],
            [sg.Button('Entrar', button_color=('white', 'green'), size=(10,2))]
        ]   
        layout = [[sg.Column(layout_column, element_justification='right')]]
        return sg.Window('Login', layout=layout, finalize=True, size=(275,150),margins=(20,15,20,20))

    def window_file():
        sg.theme('DarkBlack1')
        layout_column = [
            [sg.FileBrowse(file_types=(("Text Files", "*.txt"),), key='file', button_text='Escolher o histórico'), sg.Button('Enviar')],
            [sg.Text('', size=(125,1), font='ANY 8', key='file_historic')],
            [sg.Text('')],
            [sg.Button('Escolher', button_color=('white', 'green'), size=(10,2))]
        ]   
        layout = [[sg.Column(layout_column, element_justification='right')]]
        return sg.Window('File', layout=layout, finalize=True, size=(300,150),margins=(20,15,20,20))

    def window_loading():
        sg.theme('DarkBlack1')
        layout = [  
            [sg.Text('Carregando....', font='ANY 15')],
            [sg.Image(data=gif_image.gif.gif, key='_IMAGE_')],
        ]
        return sg.Window('Loading', layout=layout, size=(225,130),margins=(20,15,20,20))

    def pop_up():
        sg.popup('Erro de conexão/Senha ou Login incorretos')

    def window_option():
        sg.theme('DarkBlack1')
        layout_option = [
            [sg.Text('Escolha a conta: ', size=(40,1), justification='center', font='ANY 11')],
            [sg.Radio('Treino', group_id='account', key='account_practice'), 
                sg.Radio('Real', group_id='account', key='account_real')],
            [sg.Text('Escolha o tipo da opção: ', size=(40,1), justification='center', font='ANY 12')],
            [sg.Radio('Binária', group_id='option', key='option_binary'), 
                sg.Radio('Digital', group_id='option', key='option_digital')],
            [sg.Text('Valor de Entrada:', size=(18,1), font='ANY 11'), sg.Spin([i for i in range(1,1000)], initial_value = 2,key='value', size=(12,1))],
            [sg.Text('Stop Win: ', size=(18,1), font='ANY 11'), sg.Spin([i for i in range(1,1000)], initial_value = 10,key='stop_win', size=(12,1))],
            [sg.Text('Stop Loss: ', size=(18,1), font='ANY 11'), sg.Spin([i for i in range(1,1000)], initial_value = 20,key='stop_loss', size=(12,1))],
            [sg.Text('Martingale: ', size=(18,1), font='ANY 11'), sg.Spin([i for i in range(0,10)], key='martingale', size=(12,1))],
            [sg.Text('Multiplicador Martingale: ', size=(18,1), font='ANY 11'), sg.Spin([i for i in range(0,5)], key='multiplier', size=(12,1))],
            [sg.Text('')],
            [sg.FileBrowse(file_types=(("Text Files", "*.txt"),), key='file', button_text='Escolher os Sinais'), sg.Button('Enviar')],
            [sg.Listbox(values=[], size=(30,5), font='ANY 11', key='listbox')],
            [sg.Text('')],
            [sg.Button('Operar', button_color=('white', 'black'), size=(10,1))]
        ]   
        layout = [[sg.Column(layout_option, element_justification='center')]]
        return sg.Window('Options', layout=layout, finalize=True, size=(350,500),margins=(10,15,20,20))

    def window_trading(type, balance, martingale, stop_win, stop_loss):
        sg.theme('DarkBlack1')
        layout_column = [  
            [sg.Text(('Conta: Real' if type == 'REAL' else 'Conta: Treino'), font='ANY 15', justification='right', size = (40,1))],
            [sg.Text('')],
            [sg.Text('Banca: ' + str(balance), font='ANY 15', text_color='#64929E', justification='right', key = '-balance-')],
            [sg.Text('Martingale: '+ str(martingale), font='ANY 15', justification='left')],
            [sg.Text('Stop Win: ' + str(stop_win), font='ANY 15', text_color='#00994D', justification='left', key = '-stop_win-')],
            [sg.Text('Stop Loss: ' + str(stop_loss), font='ANY 15', text_color='#D93F07', justification='left',key = '-stop_loss-')],
            [sg.Text('Trabalhando ...', font='ANY 15', key = '-status-')],
            [sg.Text('')],
            [sg.Text('Próximo sinal:', font='ANY 15', justification='right')],
            [sg.Text('', key = '-signal-', size=(30,2), font='ANY 15', justification='center')],
            [sg.Button('Finalizar', button_color=('white', 'green'), size=(10,2))]
        ]
        layout = [[sg.Column(layout_column, element_justification='center')]]
        return sg.Window('Trading', layout=layout, finalize=True, size=(350,410),margins=(20,15,20,20))

    def window_finalize(balance):
        sg.theme('DarkBlack1')
        layout_column = [  
            [sg.Text(('Banca Final: ' + str(balance)), font='ANY 15', text_color='#64929E')],
            [sg.Text(('O relatorio final esta salvo na pasta:'), font='ANY 15')],
            [sg.Text(('/%appdata%/.astroend/registers'), font='ANY 15')],
            [sg.Button('Fechar', button_color=('white', 'green'))]
        ]
        layout = [[sg.Column(layout_column, element_justification='center')]]
        return sg.Window('Trading', layout=layout, finalize=True, size=(375,175),margins=(20,15,20,20))