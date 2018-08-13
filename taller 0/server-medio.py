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
		self.clients={}
		self.idIterator=0

		#Tkinter
		self.root = tkinter.Tk()
		self.root.wm_title("calculo-server-Middleware")
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

		self.list = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set)
		self.list.pack(fill=tkinter.BOTH, expand=1)

		self.buttonShowFile = tkinter.Button(frame, text='Wait new Server', command=self.waitNewServer)
		self.buttonShowFile.grid(row=2, columnspan=1)

		self.buttonShowFile = tkinter.Button(frame, text='Wait new Client', command=self.waitNewClient)
		self.buttonShowFile.grid(row=3, columnspan=1)

		self.buttonUpdate = tkinter.Button(frame, text='Update List', command=self.updateListBox)
		self.buttonUpdate.grid(row=4, columnspan=1)

		# self.buttonUpdate.config(state=tkinter.DISABLED)

		tkinter.Label(frame, text='Estado').grid(row=1, column=0)
		self.answer = tkinter.StringVar()
		self.answer.set("Ready")
		tkinter.Label(frame, textvariable=self.answer).grid(row=1, column=1)

	def yview(self, *args):
		self.TextoBox.yview(*args)
		self.TextoBox2.yview(*args)
		self.list.yview(*args)

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

	def showInfo(self):
		fileSelected=self.list.curselection()
		if(len(fileSelected)==1):
			fileName=self.list.get(fileSelected[0])

	def sendMsg(self, message, addres):
		if isinstance(message, str):
			self.sock.sendto(message.encode('utf-8'), addres)
		elif isinstance(message, bytes):
			self.sock.sendto(message, addres)
		else:
			print("ERROR - Data type to send can't work")
			return None

	def recieveMsg(self, size):
		try:
			data, addr = self.sock.recvfrom(size)
			return (data.decode('utf-8'), addr)
		except socket.timeout:
			return (None, None)

	def updateListBox(self):
		self.printBox1("Actualizando lista de servers")
		listaTemp=self.clients
		self.list.delete(0, tkinter.END)#Borra TODO
		for i in listaTemp:
			self.list.insert(tkinter.END, i+" <-> "+str(listaTemp[i]["address"]))

	def waitNewServer(self):
		self.printBox1("Creando nueva conexion")
		hilo1=threading.Thread(target=self.runConecctionServer, args=([self.idIterator]))
		self.idIterator+=1
		hilo1.start()

	def waitNewClient(self):
		self.printBox1("Creando nueva conexion")
		hilo1=threading.Thread(target=self.runConecctionClient)
		hilo1.start()

	def runConecctionClient(self):
		
		self.printBox1("Esperando conexión, id={}".format(id))
		while True:
			try:
				connection, client_address = self.sock.accept()
				connection.sendall("Ready".encode("utf-8"))#definir
				self.printBox1("conexión lista -> conecction {} addres {}".format(connection, client_address))
				break
			except socket.timeout:
				self.printBox1("cerrada id={}".format(id))
				return
			except:
				self.printBox1("Cerrado id={}".format(id))
				return
			#self.clients
		self.printBox1('conexion id={} addres={}'.format(id, client_address))
		self.printBox1("Determinando quien es")
		try:
			data = connection.recv(19).decode("utf-8")
			self.clients[data]={"connection":connection, "address":client_address}
		except socket.timeout:
			self.printBox1("cerrada id={}".format(id))
			return
		except:
			self.printBox1("Cerrado id={}".format(id))
			return
		self.updateListBox()
		# Recibe los datos en trozos y reetransmite
		while True:
			try:
				data = connection.recv(19).decode("utf-8")
			except socket.timeout:
				self.printBox("esperando nuevamente")
				continue
			except:
				self.clients.pop(data)
				self.printBox1("Se ha cerrado id={}, address={}".format(id, client_address))
				self.updateListBox()
				break
			op=None
			op1=None
			op2=None
			self.printBox1("recibido -> {}".format(data))
			correctFormat=False
			try:
				op, op1, op2=str(data).split(",")
				self.printBox2("operacion {}, op1 {}, op2 {}".format(op, op1, op2))
				correctFormat=True
				#result=eval_binary_expr(int(op1), op, int(op2))
			except:
				self.printBox1("Error id={}, address={}".format(id, client_address))
				connection.sendall("Bad format".encode("utf-8"))
			if(correctFormat):
				self.clients.get(op).get("connection").sendall(data.encode("utf-8"))
				result=self.clients.get(op).get("connection").recv(19).decode("utf-8")
				self.printBox2("resultado -> {}".format(result))
				self.printBox1("Enviando resultado={} toAddress{}".format(result, client_address))
				connection.sendall(result.encode("utf-8"))

	def runConecctionServer(self, id):
		
		self.printBox1("Esperando conexión, id={}".format(id))
		while True:
			try:
				connection, client_address = self.sock.accept()
				connection.sendall("Ready".encode("utf-8"))
				self.printBox1("conexión lista -> conecction {} addres {}".format(connection, client_address))

				break
			except socket.timeout:
				self.printBox1("cerrada id={}".format(id))
				return
			except:
				self.printBox1("Cerrado id={}".format(id))
				return
			#self.clients
		self.printBox1('conexion id={} addres={}'.format(id, client_address))
		self.printBox1("Determinando quien es")
		try:
			data = connection.recv(19).decode("utf-8")
			self.clients[data]={"connection":connection, "address":client_address}
		except socket.timeout:
			self.printBox1("cerrada id={}".format(id))
			return
		except:
			self.printBox1("Cerrado id={}".format(id))
			return
		self.updateListBox()
		# Recibe los datos en trozos y reetransmite
		while True:
			try:
				data = connection.recv(19).decode("utf-8")
			except:
				self.clients.pop(data)
				self.printBox1("Se ha cerrado id={}, address={}".format(id, client_address))
				self.updateListBox()
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
				self.printBox1("Enviando resultado={} toAddress{}".format(result, client_address))

				connection.sendall(str(result).encode("utf-8"))
			except:
				self.printBox1("Error id={}, address={}".format(id, client_address))
				connection.sendall("Error".encode("utf-8"))
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