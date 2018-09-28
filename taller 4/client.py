#!/usr/bin/env python3
import pika
import threading
import operator
import sys
import tkinter as tkinter
import time
import pika
import uuid



class rabbitmqClient:
	def __init__(self, ip="localhost"):
		#rabbitmq
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip, socket_timeout=2))
		self.channel = self.connection.channel()
		result=self.channel.queue_declare(exclusive=True)
		self.queue_name = result.method.queue
		self.channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)
		self.channel.basic_consume(self.receive, queue=self.queue_name, no_ack=True)

		#Misc
		self.correlation_id=None
		self.response=None
		
		#Tkinter
		self.root = tkinter.Tk()
		self.titleWindow="calculo-server-Multi"
		self.root.wm_title("calculo-server-Multi")
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
		tkinter.Entry(frame, textvariable=self.command).grid(row=2, column=1)

		# self.list = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set)
		# self.list.pack(fill=tkinter.BOTH, expand=1)

		self.buttonSendAdd = tkinter.Button(frame, text='+', command=self.operationAdd)
		self.buttonSendAdd.grid(row=3, column=0)

		self.buttonSendSub = tkinter.Button(frame, text='-', command=self.operationSub)
		self.buttonSendSub.grid(row=3, column=1)

		self.buttonSendMulti = tkinter.Button(frame, text='*', command=self.operationMulti)
		self.buttonSendMulti.grid(row=4, column=0)

		self.buttonSendDiv = tkinter.Button(frame, text='/', command=self.operationDiv)
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
	def operationAdd(self):
		self.answer.set("Busy-Multi")
		value=self.operation("+")
		self.printBox2("Resultado -> {}".format(value))
		self.answer.set("Ready")

	def operationSub(self):
		self.answer.set("Busy-Multi")
		value=self.operation("*")
		self.printBox2("Resultado -> {}".format(value))
		self.answer.set("Ready")
	
	def operationMulti(self):
		self.answer.set("Busy-Multi")
		value=self.operation("*")
		self.printBox2("Resultado -> {}".format(value))
		self.answer.set("Ready")
	
	def operationDiv(self):
		self.answer.set("Busy-Multi")
		value=self.operation("/")
		self.printBox2("Resultado -> {}".format(value))
		self.answer.set("Ready")

	def operation(self, op):
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
			self.printBox2("Operación solicitada -> {}{}{}".format(op1, op, op2))
			self.response = None
			self.correlation_id = str(uuid.uuid4())
			self.channel.basic_publish(exchange='', routing_key=op, properties=pika.BasicProperties(reply_to = self.queue_name, correlation_id = self.correlation_id,),body=str(value))
			while self.response is None:
				self.connection.process_data_events()
			return int(self.response)


			

	def runGraph(self):
		self.root.mainloop()

	def receive(self, ch, method, properties, body):
		
		if self.correlation_id == properties.correlation_id:
			body=body.decode("utf-8")
			self.printBox2("resultado {}".format(body))
			self.response = body
			

if __name__ == '__main__':
	servidor=rabbitmqClient()
	print("Server iniciado")
	servidor.runGraph()