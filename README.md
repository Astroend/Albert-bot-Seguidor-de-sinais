# Seguidor de sinais Open Source
Desenvolvido pela equipe Astroend.

## Objetivo.

Este projeto consiste em um automatizador que segue sinais passados a ele em um txt,
onde o mesmo, lê o bloco de notas e assim, recebe as instruções de entradas.

## Biblioteca utilizada.

A biblioteca utilizada para a leitura da corretora foi a [Iqoptionapi](https://github.com/Lu-Yi-Hsun/iqoptionapi), desenvolvida
por [Lu-Yi-Hsun](https://github.com/Lu-Yi-Hsun) que é de fácil acesso e de fácil entendimento.


## Funcionamento do Automatizador.

### Leitura do arquivo txt.

A classe ReadTXT é responsável pela leitura e conversão dos sinais contidos no arquivo TXT para um dicionário com índices em strings,
separando cada elemento no sinal com seu propósito único (Duração, Horário, Paridade e direção) para um aproveitamento mais simplificado
no percorrer do código.

Os sinais podem ser colocados em quaisquer ordens desejadas, tendo apenas que ser separado por " - " ( Exemplo: "M5-14:30-EURUSD-PUT").

##### Alteração, no formato de sinais.
O formato da lista de sinais agora tem suporte para valores de data como
"M5-14:30-EURUSD-PUT-05/10" os valores continuam sendo separados por "-" 
e podem estar em qualquer ordem para maior flexibilidade.

O arquivo txt depois de lido é convertido para o padrão de Dicionário presente nativamente no Python.
