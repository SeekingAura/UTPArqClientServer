import threading
import socket
import operator
import sys
import tkinter as tkinter
import time
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

class TCPSocketServer:
	def __init__(self, ip, puerto):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # UDP
		self.ip=ip
		self.puerto=puerto
		# ipvalue=socket.gethostname()
		self.sock.bind((ip, puerto))
		# print("ip value -> ", ipvalue)
		# Escuchando conexiones entrantes
		self.sock.listen(10)
		self.sock.settimeout(30)#Establecer tiempo limite de espera en segundos por cada recvfrom
		self.clients=[]
		self.idIterator=0

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

		self.buttonConecctServer = tkinter.Button(frame, text='Connect to Server', command=self.createConecction)
		self.buttonConecctServer.grid(row=2, columnspan=1)

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
	def sendMsg(self, message, sock, to="", trys=50):
		trysCount=0
		while trysCount<trys:
			try:
				self.printBox1("enviado mensaje={}, to={}".format(message, to))
				sock.sendall(str(message).encode("utf-8"))
				return True
			except socket.timeout:
				print("tiempo superado de envio message={}, to={}, try#={}".format(message, to, trysCount))
			except:
				print("Error al enviar mensaje={}, to={}".format(message, to))
				return False
			trysCount+=1

	

	def recvMsg(self, sock, to="", bytesBuffer=1024,trys=50):
		trysCount=0
		while trysCount<trys:
			try:
				received=sock.recv(bytesBuffer).decode("utf-8")
				self.printBox1("reciviendo message={}, from={}".format(received, to))
				return received
			except socket.timeout:
				print("tiempo superado de recibido to={}, try#={}".format(to, trysCount))
			except:
				print("Error al recibir to={}".format(to))
				return None
			trysCount+=1

	# def updateListBox(self):
	# 	self.printBox1("Actualizando lista de servers")
	# 	listaTemp=self.clients
	# 	self.list.delete(0, tkinter.END)#Borra TODO
	# 	for i in listaTemp:
	# 		self.list.insert(tkinter.END, i)

	def createConecction(self):
		self.printBox1("Conectando a server")
		self.answer.set("Coneccting...")
		message=self.command.get()
		try:
			ipServer, puertoServer=message.split(", ")
			puertoServer=int(puertoServer)
		except:
			self.printBox1("Conexión fallida")
			self.printBox1("Formato mal escrito, se esperaba formato ###.###.###.###, #####")
			self.answer.set("Ready")
			return
		self.command.set("")
		hilo1=threading.Thread(target=self.runConecctions, args=([ipServer, puertoServer]))
		self.idIterator+=1
		hilo1.start()

	def runConecctions(self, ipServer, puertoServer):
		# self.sock.connect((self.ip, self.puerto))
		sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((ipServer, puertoServer))
		except:
			print("fallo al conectar")
			return
		self.answer.set("Setting ID")
		data = self.recvMsg(sock, to=str((ipServer, puertoServer)))
		self.root.wm_title(self.titleWindow+" - "+data)
		self.answer.set("Sending Who am i")
		self.sendMsg("*", sock, to=str((ipServer, puertoServer)))

		data = self.recvMsg(sock, to=str((ipServer, puertoServer)))
		self.printBox2("ip recibida -> {}".format(data))
		self.sendMsg(str(self.puerto), sock, to=str((ipServer, puertoServer)))
		self.answer.set("Waiting for conecction server")
		# Recibe los datos en trozos y reetransmite
		try:
			connection, client_address = self.sock.accept()
			self.printBox1("Conectado a servidor")
		except:
			self.answer.set("Ready")
			self.printBox1("ERROR cuando conectó el middleware")
			return
		self.answer.set("Ready")
		while True:
			data = self.recvMsg(connection, to=str(client_address))

			if(data is None):
				# self.clients.remove(client_address)
				# self.printBox1("Se ha cerrado id={}, address={}".format(id, client_address))
				# self.updateListBox()
				self.printBox1("Error de conexión con el server={}, cerrando".format(client_address))
				break
			
			op=None
			op1=None
			op2=None

			self.printBox1("recibido -> {}".format(data))
			try:
				op, op1, op2=str(data).split(",")
				self.printBox2("operacion {}, op1 {}, op2 {}".format(op, op1, op2))
				result=eval_binary_expr(int(op1), op, int(op2))
				self.printBox2("resultado -> {}".format(result))
				self.sendMsg(str(result), connection, to=str(client_address))
			except:
				self.sendMsg("Error", connection, to=str(client_address))
	def runGraph(self):
		self.root.mainloop()

if __name__ == '__main__':
	ipServer = input("Ingrese la ip del server -> ")
	puertoServer = int(input("ingrese el puerto del server -> "))
	print("server IP:", ipServer)
	print("server port:", puertoServer)
	servidor=TCPSocketServer(ipServer, puertoServer)
	print("Server iniciado")
	servidor.runGraph()