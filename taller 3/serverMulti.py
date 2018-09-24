import threading
import operator
import sys
import tkinter as tkinter
import time
import pika
import threading

def get_operator_fn(op):
	return {
		'+' : operator.add,
		'-' : operator.sub,
		'*' : operator.mul,
		'/' : operator.truediv,
		'MOD' : operator.mod,
		'^' : operator.xor,
		}[op]

def eval_binary_expr(op1, operator, op2):
	op1,op2 = int(op1), int(op2)
	return get_operator_fn(operator)(op1, op2)


class rabbitmqServer:
	def __init__(self, ip="192.168.8.247"):
		#rabbitmq
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip, socket_timeout=2))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='*')
		self.channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)
		self.channel.basic_consume(self.operationMul, queue='*', no_ack=True)


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

		#self.command = tkinter.StringVar()
		#tkinter.Entry(frame, textvariable=self.command).grid(row=2, column=1)

		# self.list = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set)
		# self.list.pack(fill=tkinter.BOTH, expand=1)

		# self.buttonConecctServer = tkinter.Button(frame, text='Start', command=self.runServer)
		# self.buttonConecctServer.grid(row=2, columnspan=1)

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

	#Can sock connection or sock
	def operationMul(self, ch, method, properties, body):
		op1=None
		op2=None
		queueValue=None
		body=body.decode("utf-8")
		self.printBox1("recibido -> {}".format(body))
		result=None
		try:
			queueValue, op1, op2=str(body).split(", ")
			self.printBox2("operacion op1*op2 -> {}*{} ->".format(op1, op2))
			result=eval_binary_expr(int(op1), "*", int(op2))
			self.printBox2("resultado -> {}".format(result))
		except:
			self.printBox1("Error queueClient {}, op1 {}, op2 {}".format(queueValue, op1, op2))

		if(queueValue is not None):
			try:
				if(op1 is not None and op2 is not None and result is not None):
					self.channel.basic_publish(exchange='', routing_key=queueValue, body=op1+"*"+op2+"="+str(result))
					self.printBox2("enviado -> {}".format(result))
				else:
					channel.basic_publish(exchange='', routing_key=queueValue, body="Error en su formato!")
					self.printBox2("enviado -> {}".format("Error en su formato!"))
			except:
				self.printBox1("No fue posible enviar, queue {}".format(queueValue))
	def runServer(self):
		self.channel.start_consuming()
	def runGraph(self):
		self.root.mainloop()

if __name__ == '__main__':
	servidor=rabbitmqServer()
	print("Server iniciado")
	hilo1=threading.Thread(target=servidor.runServer)
	hilo1.start()
	servidor.runGraph()