#!/usr/bin/env python3

import pika
import uuid

import threading
import os
import sys
import time

import tkinter as tkinter
import pygame



class rabbitmqServer:
	def __init__(self, ip="localhost"):
		#rabbitmq
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip, socket_timeout=2))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='conectoSitio')
		self.channel.queue_declare(queue='conectoCliente')
		
		self.listSitios=["Sitios"]
		self.listClientesWeb=["Clientes Web"]
		self.listClientesAPP=["Clientes App"]
		
		#Tkinter
		self.root = tkinter.Tk()
		self.root.wm_title("Servicio de Reproducción")
		scrollbar = tkinter.Scrollbar(self.root, orient=tkinter.VERTICAL)
		self.textoBox = tkinter.Text(self.root, height=8, width=45, yscrollcommand=scrollbar.set)# controla el tamaño del Textobox
		self.textoBox2 = tkinter.Text(self.root, height=8, width=45, yscrollcommand=scrollbar.set)# controla el tamaño del Textobox2
		scrollbar.config(command=self.yview)
		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		
		self.textoBox.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.textoBox.config(state=tkinter.DISABLED)
		self.textoBox2.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.textoBox2.config(state=tkinter.DISABLED)
		frame = tkinter.Frame(self.root)
		frame.pack()

		#list
		self.list = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set, exportselection=False)
		self.list2 = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set, exportselection=False)
		self.list3 = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set, exportselection=False)
		#self.list.bind('<<ListboxSelect>>', self.showInfoSong)
		self.list.pack(fill=tkinter.BOTH, expand=1)
		self.list2.pack(fill=tkinter.BOTH, expand=1)
		self.list3.pack(fill=tkinter.BOTH, expand=1)

		# self.command = tkinter.StringVar()
		# tkinter.Entry(frame, textvariable=self.command).grid(row=1, column=1)
		tkinter.Label(frame, text='State:').grid(row=0, column=0)
		self.answer = tkinter.StringVar()
		self.answer.set("Stoped")
		tkinter.Label(frame, textvariable=self.answer).grid(row=0, column=1)

		

		self.buttonUpdate = tkinter.Button(frame, text='Update List', command=self.updateListBox)
		self.buttonUpdate.grid(row=1, column=0, columnspan=1)

		# self.buttonUpdate.config(state=tkinter.DISABLED)

		
		

	def yview(self, *args):
		self.textoBox.yview(*args)
		self.textoBox2.yview(*args)
		self.list.yview(*args)

	def printBox1(self, value):# Maneja el log
		self.textoBox.config(state=tkinter.NORMAL)
		self.textoBox.insert(tkinter.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.textoBox.see(tkinter.END)
		self.textoBox.config(state=tkinter.DISABLED)

	def printBox2(self, value):
		self.textoBox2.config(state=tkinter.NORMAL)
		self.textoBox2.delete('1.0', tkinter.END)
		self.textoBox2.insert(tkinter.END, str(value))
		self.textoBox2.see(tkinter.END)
		self.textoBox2.config(state=tkinter.DISABLED)

	def deletePrintBox2(self, value):
		self.textoBox2.config(state=tkinter.NORMAL)
		self.textoBox2.delete('1.0', tkinter.END)
		self.textoBox2.see(tkinter.END)
		self.textoBox2.config(state=tkinter.DISABLED)
		
	def updateListBox(self):
		self.list.delete(0, tkinter.END)#Borra TODO
		for lugar in self.listSitios:
			self.list.insert(tkinter.END, lugar)
		self.list2.delete(0, tkinter.END)#Borra TODO
		for lugar in self.listClientesWeb:
			self.list2.insert(tkinter.END, lugar)
		self.list3.delete(0, tkinter.END)#Borra TODO
		for lugar in self.listClientesAPP:
			self.list3.insert(tkinter.END, lugar)
		


	def createTempQueue(self):
		result=self.channel.queue_declare(exclusive=True)#temporal queue
		queueName = result.method.queue
		self.channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)
		self.channel.basic_consume(self.receive, queue=self.queueName, no_ack=True)
		return queueName
	
	def receive(self, ch, method, properties, body):
		self.printBox1("Mensaje recibido {}".format(body.decode("utf-8")))
		self.printBox2("resultado {}".format(body.decode("utf-8")))

	
	def runReceive(self):
		self.channel.start_consuming()

	def runGraph(self):
		# self.buttonUpdate.after(1000, self.connectReceive)
		self.root.mainloop()

	

if __name__ == '__main__':
	servidor=rabbitmqClient()
	hilo1=threading.Thread(target=servidor.runReceive)
	hilo1.start()
	print("Server iniciado")
	servidor.runGraph()