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
    print( '# cadidatos : opcoes de voto        #' )
    print( '# V (numero): votar candidato       #' )
    print( '# B : votar branco                  #' )
    print( '# N : votar nulo                    #' )
    print( '# ajuda : Mostrar uso dos comandos  #' )
    print( '# fechar : Encerrar conexão         #' )
    print('#####################################\n')

def tryInputClientTypeFuel(mensagem):
    if mensagem[0] == 'V' or mensagem[0] == 'B' or mensagem[0] == 'N' :
        return True
    
    return False

def tryInputClientCommand(mensagem):
    
    if mensagem[0] == 'V' or mensagem[0] == 'B' or mensagem[0] == 'N' or mensagem[0] == 'cadidatos' or mensagem[0] == 'print' :
        return True
    return False
    
def tratamentosClient(dadosMensagem):
    tamanhoDaMensagem = len(dadosMensagem)
    if tryInputClientCommand(dadosMensagem) == False:
        print("\nPor favor, verifique se o comando digitado esta correto\n")
        return True
    # elif tryInputClientTypeFuel(dadosMensagem) == False and dadosMensagem[1] != 'all':
    #     print("\nEsse valor para combustivel não é valido!\n")
    #     print("0 para Disel\n1 para álcool\n2 para gasolina\n")
    #     return True
    elif tamanhoDaMensagem != 2:
        if dadosMensagem[1] == 'all': return False
        elif tamanhoDaMensagem < 2: print('\nAtenção\nEsta faltando dados de entrada\n')
        else: print('\nAtenção\nVocê inseriu dados a mais\n')
        return True
    return False

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

            # Faz tratamento pelo client verificando condicoes de entrada
            if tratamentosClient(dadosMensagem):
                mensagem = ""
                continue

            idMensagem = dadosMensagem[1]

            udp.sendto(str.encode(mensagem), dest)
            data = udp.recv(1024)

            if data.decode()!= 'all':
                # mensagem recebida do servidor
                print("Recebido: {}".format(data.decode()))
            
            # reenviar mensagem
            if data.decode()!= idMensagem: udp.sendto(str.encode(mensagem), dest)          
        
        mensagem = input("Digite seu comando: ") 

    udp.close()


if __name__ == "__main__":
    main()