#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################################################
# File name: server.py                                                                               #
######################################################################################################
# author: Lauro Milagres Oliveira                                                                    #
# author: Lucas Dutra Donoso Ponce de Leon                                                           #
######################################################################################################
# Trabalho pratico - Questao 2 (Sistema de votacao para melhor professor)                            #
#                                                                                                    #
# Objetivo:                                                                                          #
# O servidor deve confirmar a recepcao de mensagens.                                                 #
# O servidor deve adicionar a informacao em um arquivo. (votacoes.in)                                #
# O servidor deve retornar o resultado das votacoes (quantidade de votos por professor  )            #
# O servidor deve imprimir na tela o conteudo das mensagens que eles receberem.                      #
#                                                                                                    #
######################################################################################################

import socket
import os.path

from time import sleep
import sys

# Endereco IP do Servidor
HOST = ''
# Porta que o Servidor esta                                     
PORT = input("Insira a porta: ")

# Tratamento para porta do servidor, a porta deve ser valida
# neste caso que seja apenas digito
inputValidation = False

# Modo grosseiro de verificacao
while inputValidation == False:

    if PORT.isdigit():
        inputValidation = True
    else:
        print("ERRO! Porta Invalida")
        PORT = input(">>> Informar porta: ")


udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, int(PORT))
udp.bind(orig)


def verifyExistsFile():
    return os.path.exists('votacoes.in')

def writeFile(comando):
    try:
        arq = open("votacoes.in", "a")
        
        if len(comando) > 1:
        
            if(comando[1] == '558200'):
                arq.write(comando[1] + " - Marco Antonio da Silva Barbosa")
            elif(comando[1] == '558201'):
                arq.write(comando[1] + " - Raquel Aparecida de Freitas Mini")
            elif(comando[1] == '558202'):
                arq.write(comando[1] + " - Carlos Alberto Marques Pietrobon")
            elif(comando[1] == '558203'):
                arq.write(comando[1] + " - Maria Lourdes Granha Nogueira")
            elif(comando[1] == '558204'):
                arq.write(comando[1] + " - Max Do Val Machado")
            elif(comando[1] == '558205'):
                arq.write(comando[1] + " - Felipe Domingos da Cunha")
            else:   
                print('Nenhum candidato com esse id foi encontrado.\n')
        else:
            if(comando[0] == 'B'):
                arq.write(comando[0] + " - Voto Branco")
            elif(comando[0] == 'N'):
                arq.write(comando[0] + " - Voto Nulo")
        arq.write("\n")
        arq.close()
        print('Votação concluída com sucesso!\n')
    except:
        print('Algo de errado aconteceu, tente novamente!')

def printFile():
    try:
        arq =  open("votacoes.in", "r")
        print('################################################################')
        print('#                        ORDEM DE VOTOS                        #')
        print('################################################################\n')
        c558200 = 0
        c558201 = 0
        c558202 = 0
        c558203 = 0
        c558204 = 0
        c558205 = 0
        cbranco = 0
        cnulo = 0
        for line in arq:
            candidato = line.split(" - ")
            print(line)
            if(candidato[0] == '558200'): c558200 += 1
            elif(candidato[0] == '558201'): c558201 += 1
            elif(candidato[0] == '558202'): c558202 += 1
            elif(candidato[0] == '558203'): c558203 += 1
            elif(candidato[0] == '558204'): c558204 += 1
            elif(candidato[0] == '558205'): c558205 += 1
            elif(candidato[0] == 'B'): cbranco += 1
            elif(candidato[0] == 'N'): cnulo += 1
        print('\n###############################################################')
        print('#                      Parcial dos votos                      #')
        print('###############################################################')
        print("Marco Antonio da Silva Barbosa - " + str(c558200) + " votos.")
        print("Raquel Aparecida de Freitas Mini - " + str(c558201) + " votos.")
        print("Carlos Alberto Marques Pietrobon - " + str(c558202) + " votos.")
        print("Maria Lourdes Granha Nogueira - " + str(c558203) + " votos.")
        print("Max Do Val Machado - " + str(c558204) + " votos.")
        print("Felipe Domingos da Cunha - " + str(c558205) + " votos.")
        print('###############################################################')
        print("Branco - " + str(cbranco) + " votos.")
        print("Nulo - " + str(cnulo) + " votos.")
        print('###############################################################')
    except IOError:
        print('Arquivo não encontrado!')

def loadingdServer():
    
    for i in range(21):
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
        sys.stdout.flush()
        sleep(0.25)
    
    print("\n\nServidor Conectado\n")


def main():
    
    loadingdServer()
    
    while True:

        msg, cliente = udp.recvfrom(1024)
        
        if not msg: break
        
        comando = msg.decode().split( )

        comandoPrincipal = comando[0]
        response = comando[0]

        if comandoPrincipal == 'V' or comandoPrincipal == 'B' or comandoPrincipal == 'N':
            writeFile(comando)
            printFile()

        udp.sendto(str.encode(response), cliente)    

    udp.close()


if __name__ == "__main__":
    main()