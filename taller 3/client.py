#!/usr/bin/env python3
import sys
import tkinter as tkinter
import time
import pika
import threading



class rabbitmqClient:
	def __init__(self, ip="192.168.10.214", name="0"):
		#rabbitmq
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip, socket_timeout=2))
		self.channel = self.connection.channel()
		result=self.channel.queue_declare(exclusive=True)
		self.queue_name = result.method.queue
		self.channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)
		self.channel.basic_consume(self.receive, queue=self.queue_name, no_ack=True)


		#Tkinter
		self.nameClient=name
		self.root = tkinter.Tk()
		self.titleWindow="calculo-Cliente"+self.nameClient
		self.root.wm_title(self.titleWindow)
		scrollbar = tkinter.Scrollbar(self.root, orient=tkinter.VERTICAL)
		self.TextoBox = tkinter.Text(self.root, height=8, width=80, yscrollcommand=scrollbar.set)
		self.TextoBox2 = tkinter.Text(self.root, height=8, width=80, yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.yview)
		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		
		self.TextoBox.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.TextoBox.config(state=tkinter.DISABLED)
		self.TextoBox2.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.TextoBox2.config(state=tkinter.DISABLED)
		frame = tkinter.Frame(self.root)
		frame.pack()

		self.command = tkinter.StringVar()
		tkinter.Label(frame, text='operations').grid(row=2, column=0)
		tkinter.Entry(frame, textvariable=self.command).grid(row=2, column=1)

		# self.list = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set)
		# self.list.pack(fill=tkinter.BOTH, expand=1)

		self.buttonSendPlus = tkinter.Button(frame, text='+', command=self.sendMessageSum)
		self.buttonSendPlus.grid(row=3, column=0)
		self.buttonSendSub = tkinter.Button(frame, text='-', command=self.sendMessageSub)
		self.buttonSendSub.grid(row=3, column=1)
		self.buttonSendMulti = tkinter.Button(frame, text='*', command=self.sendMessageMulti)
		self.buttonSendMulti.grid(row=4, column=0)
		self.buttonSendDiv = tkinter.Button(frame, text='/', command=self.sendMessageDiv)
		self.buttonSendDiv.grid(row=4, column=1)

		#self.buttonUpdate = tkinter.Button(frame, text='Update List', command=self.updateListBox)
		#self.buttonUpdate.grid(row=3, columnspan=1)

		# self.buttonUpdate.config(state=tkinter.DISABLED)

		tkinter.Label(frame, text='Estado').grid(row=1, column=0)
		self.answer = tkinter.StringVar()
		self.answer.set("Ready")
		tkinter.Label(frame, textvariable=self.answer).grid(row=1, column=1)
		

	def yview(self, *args):
		self.TextoBox.yview(*args)
		self.TextoBox2.yview(*args)
		# self.list.yview(*args)

	def printBox1(self, value):
		self.TextoBox.config(state=tkinter.NORMAL)
		self.TextoBox.insert(tkinter.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.TextoBox.see(tkinter.END)
		self.TextoBox.config(state=tkinter.DISABLED)

	def printBox2(self, value):
		self.TextoBox2.config(state=tkinter.NORMAL)
		self.TextoBox2.insert(tkinter.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.TextoBox2.see(tkinter.END)
		self.TextoBox2.config(state=tkinter.DISABLED)
		"""
		self.TextoBox2.config(state=tkinter.NORMAL)
		self.TextoBox2.delete('1.0', tkinter.END)
		self.TextoBox2.insert(tkinter.END, str(value))
		self.TextoBox2.see(tkinter.END)
		self.TextoBox2.config(state=tkinter.DISABLED)
		"""
	def sendMessageSum(self):
		self.answer.set("Operating [+]")
		self.sendMessage("+")
		self.answer.set("Ready")
	
	def sendMessageSub(self):
		self.answer.set("Operating [-]")
		self.sendMessage("-")
		self.answer.set("Ready")

	def sendMessageMulti(self):
		self.answer.set("Operating [*]")
		self.sendMessage("*")
		self.answer.set("Ready")
	
	def sendMessageDiv(self):
		self.answer.set("Operating [/]")
		self.sendMessage("/")
		self.answer.set("Ready")

	#Can sock connection or sock
	def sendMessage(self, op):
		value=self.command.get()
		op1=None
		op2=None
		try:
			op1, op2=value.split(", ")
		except:
			self.printBox1("Mal formato")
		if(op1 is not None and op2 is not None):
			self.command.set("")
			message=self.queue_name+", "+value
			self.channel.basic_publish(exchange='', routing_key=op,body=message)
			self.printBox1("Mensaje enviado {}".format(message))
			self.printBox2("Operación solicitada -> {}{}{}".format(op1, op, op2))

	def runReceive(self):
		self.channel.start_consuming()
	def runGraph(self):
		self.root.mainloop()

	def receive(self, ch, method, properties, body):
		self.printBox1("Mensaje recibido {}".format(body.decode("utf-8")))
		self.printBox2("resultado {}".format(body.decode("utf-8")))

if __name__ == '__main__':
	servidor=rabbitmqClient()
	print("Cliente iniciado")
	if(len(sys.argv)>1):
		hilo1=threading.Thread(target=servidor.runReceive, name=sys.argv[1])
	else:
		hilo1=threading.Thread(target=servidor.runReceive)
	hilo1.start()
	servidor.runGraph()