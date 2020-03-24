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
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
#from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

udp = socket.socket()
destino =  ('127.0.0.1', 8080)
udp.connect(destino)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Sistema de votação - PUC Minas'
        self.left = 10
        self.top = 10
        self.width = 370
        self.height = 370
        self.initUI()
        self.dest = ('127.0.0.1', 8080)
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Endereço de IP
        self.label = QLabel("IP : ", self)
        self.label.move(20,20)
        self.textbox = QLineEdit(self)
        self.textbox.move(80, 20)
        self.textbox.resize(260,30)
        self.textbox.setText("127.0.0.1")

        #Porta do servidor
        self.label2 = QLabel("Porta : ", self)
        self.label2.move(20,60)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(80, 60)
        self.textbox2.resize(260,30)
        self.textbox2.setText("8080")

        #Codigo do candidato
        self.label3 = QLabel("código: ", self)
        self.label3.move(20,100)
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(80, 100)
        self.textbox1.resize(260,30)
        
        # Create a button in the window
        self.button = QPushButton('Branco', self)
        self.button.move(20,140)
        self.button.setStyleSheet("background-color: white")

        # Create a button in the window
        self.button1 = QPushButton('Confirmar', self)
        self.button1.move(130,140)
        self.button1.setStyleSheet("background-color: green")

        # Create a button in the window
        self.button2 = QPushButton('Nulo', self)
        self.button2.move(240,140)
        self.button2.setStyleSheet("background-color: red")
        
        # Candidatos
        self.label4 = QLabel("558200 - Marco Antonio da Silva Barbosa", self)
        self.label4.move(20,200)
        self.label4.resize(300,30)

        self.label5 = QLabel("558201 - Raquel Aparecida de Freitas Mini", self)
        self.label5.move(20,220)
        self.label5.resize(300,30)

        self.label6 = QLabel("558202 - Carlos Alberto Marques Pietrobon", self)
        self.label6.move(20,240)
        self.label6.resize(300,30)

        self.label7 = QLabel("558203 - Maria Lourdes Granha Nogueira", self)
        self.label7.move(20,260)
        self.label7.resize(300,30)
        
        self.label8 = QLabel("558204 - Max Do Val Machado", self)
        self.label8.move(20,280)
        self.label8.resize(300,30)        
        
        self.label9 = QLabel("558205 - Felipe Domingos da Cunha", self)
        self.label9.move(20,300)
        self.label9.resize(300,30)

        self.labelcodigo = QLabel("Código dos candidatos", self)
        self.labelcodigo.move(20,180)
        self.labelcodigo.resize(300,30)         
        
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
        # connect button to function on_click
        self.button1.clicked.connect(self.on_click_confirm)
        self.show()
        # connect button to function on_click
        self.button2.clicked.connect(self.on_click_nulo)
        self.show()


    
    @pyqtSlot()
    def on_click(self):
        
        idMensagem = 'B'
        mensagem = 'B'

        udp.sendto(str.encode(mensagem), self.dest)
        data = udp.recv(1024)

        if data.decode()!= 'candidatos':
            print("Recebido: {}".format(data.decode()))
            # mensagem recebida do servidor
            #QMessageBox.question(self, 'Votação Encerrada', "Obrigado por votar! ", QMessageBox.Ok, QMessageBox.Ok)
        
        # reenviar mensagem
        #if data.decode()!= idMensagem: udp.sendto(str.encode(mensagem), self.dest)

        #dp.close()

    @pyqtSlot()
    def on_click_nulo(self):
        
        idMensagem = 'N'
        mensagem = 'N'

        udp.sendto(str.encode(mensagem), self.dest)
        data = udp.recv(1024)

        if data.decode()!= 'candidatos':
            print("Recebido: {}".format(data.decode()))


    @pyqtSlot()
    def on_click_confirm(self):
        
        idMensagem = 'V'
        mensagem = 'V ' + self.textbox1.text()

        udp.sendto(str.encode(mensagem), self.dest)
        data = udp.recv(1024)

        if data.decode()!= 'candidatos':
            print("Recebido: {}".format(data.decode()))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())