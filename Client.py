#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################################################
# File name: client.py                                                                               #
######################################################################################################
# author: Lauro Milagres Oliveira                                                                    #
# author: Lucas Dutra Donoso Ponce de Leon                                                           #
######################################################################################################
# Trabalho pratico - Questao 2 (Sistema de votacao para melhor professor)                            #
#                                                                                                    #
#                                                                                                    #
# O cliente envia mensagens ao servidor: votar candidato (V), votar branco (B) e votar nulo (N).     #
# O cliente deve implementar pelo menos uma retransmissão.                                           #
# Votar candidato: V idCandidato                                                                     #
# Votar branco: B                                                                                    #
# Votar nulo: N                                                                                      #
######################################################################################################


import socket



# Endereco IP do Servidor
HOST = input("Insira o endereço IP: ")
# Porta do Servidor
PORT = input("Insira a porta: ")

inputValidation = False

# Modo grosseiro de verificacao
while inputValidation == False:
    # processo de verificacao
    hostSplit = HOST.split('.')

    if len(hostSplit) != 4 and PORT.isdigit():
        print("\nErro ao definir IP")
        HOST = input(">>> Informe o IP: ")
    elif not PORT.isdigit() and len(hostSplit) == 4:
        print("\nErro ao definir porta")
        PORT = input(">>> Informe a porta: ")
    elif not PORT.isdigit() and len(hostSplit) != 4:
        print("\nErro ao definir IP e Porta")
        HOST = input(">>> Informe o IP: ")
        PORT = input(">>> Informe a porta: ")
    else:
        inputValidation = True

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, int(PORT))


def comandos():
    # comandos
    print('\n#####################################')
    print( '#              COMANDOS             #' )
    print( '#####################################' )
    print( '# candidatos : opcoes de voto       #' )
    print( '# V (numero): votar candidato       #' )
    print( '# B : votar branco                  #' )
    print( '# N : votar nulo                    #' )
    print( '# ajuda : Mostrar uso dos comandos  #' )
    print( '# fechar : Encerrar conexão         #' )
    print('#####################################\n')



"""def tryInputClientTypeFuel(mensagem):
    if mensagem[0] == 'V' or mensagem[0] == 'B' or mensagem[0] == 'N' :
        return True
    
    return False
"""
def printFile():
    try:
        arq =  open("candidatos.in", "r")
        print('\n################################################################')
        print('#                      TABELA DE CANDIDATOS                    #')
        print('################################################################\n')

        for line in arq:
            print(line)
        print('################################################################\n')
    except IOError:
        print('Arquivo não encontrado!')

def tryInputClientCommand(mensagem):
    if mensagem[0] == 'V' or mensagem[0] == 'B' or mensagem[0] == 'N' or mensagem[0] == 'candidatos' :
        return True
    return False
    
def tratamentosClient(dadosMensagem):
    tamanhoDaMensagem = len(dadosMensagem)
    print("\nMensagem : ", dadosMensagem)
    print("Tamanho da mensagem : ", tamanhoDaMensagem)
    print("================================================\n")
    if tryInputClientCommand(dadosMensagem) == False:
        print("\nPor favor, verifique se o comando digitado esta correto\n")
        return True
    elif tryInputClientCommand(dadosMensagem): return False
    elif tamanhoDaMensagem < 1: print('\nAtenção\nEsta faltando dados de entrada\n')
    elif tamanhoDaMensagem > 2: print('\nAtenção\nVocê inseriu dados a mais\n')
    
    return True

def main():
    # iniciando tabela com comandos
    comandos()
    mensagem = input("Digite seu comando: ")

    while mensagem != '\x18':
        
        if mensagem == 'fechar': break
        
        if mensagem == 'ajuda':
            comandos()
            mensagem = ''
            continue
        
        if mensagem == "":
            pass
        else:
            
            dadosMensagem = mensagem.split( )

            print("1 - dadosMensagem : ", dadosMensagem)
            print("2 - tamanho do dadosMEnsagem : ", len(dadosMensagem))

            # Faz tratamento pelo client verificando condicoes de entrada
            if tratamentosClient(dadosMensagem):
                print("Entrei no if do primeiro tratamento")
                mensagem = ""
                continue
            elif dadosMensagem[0] == 'candidatos':
                printFile()
                mensagem = ""
                continue
            
            idMensagem = dadosMensagem[0]

            #print("dadosMensagem ====> ", dadosMensagem)
            #print("idMensagem ====> ", idMensagem)
            
            
            if idMensagem == 'V' or idMensagem == 'B' or idMensagem == 'N':

                udp.sendto(str.encode(mensagem), dest)
                data = udp.recv(1024)

                print("data => ", data)

                if data.decode()!= 'candidatos':
                    # mensagem recebida do servidor
                    print("Recebido: {}".format(data.decode()))
                
                # reenviar mensagem
                if data.decode()!= idMensagem: udp.sendto(str.encode(mensagem), dest)

                print("\nVotação Encerrada. Obrigado pelo seu voto! \n")
                break
        
        mensagem = input("Digite seu comando: ") 

    udp.close()


if __name__ == "__main__":
    main()