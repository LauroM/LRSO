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
import os.path
from time import sleep
import sys
import socket
import threading

class Server(object):
	#Construtores 
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        #print("CONSTRUTOR")

    def listen(self):
        self.sock.listen(500)
        self.loadingdServer()
        while True:
            #aceitar a conexão do cliente
            client, address = self.sock.accept()
            print("Cliente conectado",address)
            # Tempo de vida de cada thread
            client.settimeout(550)
            #Criacao das thread para cada client no server
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def verifyExistsFile(self):
        return os.path.exists('votacoes.in')

    def writeFile(self,comando):
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

    def printFile(self):
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

    def loadingdServer(self):
        
        for i in range(21):
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
            sys.stdout.flush()
            sleep(0.25)
        
        print("\n\nServidor Conectado\n")
	
	#MultiThreading
    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                #Mensagem recebida do lado do Cliente
                data = client.recv(size)
                
                # primeira verificacao de dado
                if data:
                
                    comando = data.decode().split( )
                    comandoPrincipal = comando[0]
                    response = comando[0]
                    # caso a mensagem recebida do client possua esses tres comandos principais
                    # se possuir, abre o metodo writeFile para escrita no arquivo e gerar nosso log
                    # depois mostra o log junto com as parciais dos votos
                    if comandoPrincipal == 'V' or comandoPrincipal == 'B' or comandoPrincipal == 'N':
                        self.writeFile(comando)
                        self.printFile()
            except:
                client.close()
                return False

if __name__ == "__main__":
    
    inputPort = input("Insira a porta: ")
    while True:
        try:
            inputPort = int(inputPort)
            break
        except ValueError:
            pass
    Server('',inputPort).listen()