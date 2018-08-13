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
		# self.sock.bind((ip, puerto))
		# print("ip value -> ", ipvalue)
		# Escuchando conexiones entrantes
		# self.sock.listen(10)
		self.sock.settimeout(30)#Establecer tiempo limite de espera en segundos por cada recvfrom
		self.clients=[]
		self.idIterator=0

		#Tkinter
		self.root = tkinter.Tk()
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

		self.list = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set)
		self.list.pack(fill=tkinter.BOTH, expand=1)

		self.buttonShowFile = tkinter.Button(frame, text='Wait new', command=self.waitNew)
		self.buttonShowFile.grid(row=2, columnspan=1)

		self.buttonUpdate = tkinter.Button(frame, text='Update List', command=self.updateListBox)
		self.buttonUpdate.grid(row=3, columnspan=1)

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
			self.list.insert(tkinter.END, i)

	def waitNew(self):
		self.printBox1("Conectando a server")
		hilo1=threading.Thread(target=self.runConecctions)
		self.idIterator+=1
		hilo1.start()
	def runConecctions(self):
		ipServer = input("Ingrese la ip del server intermedio -> ")
		puertoServer = int(input("ingrese el puerto del server intermedio -> "))
		# self.sock.connect((self.ip, self.puerto))
		self.sock.connect((ipServer, puertoServer))
		
		try:
			data = self.sock.recv(19).decode("utf-8")
			# self.wm_title+=" - "+data
			# self.root.wm_title(self.wm_title)
			self.sock.sendall("*".encode("utf-8"))
		except:
			print("Failed conecction")
			return
		# Recibe los datos en trozos y reetransmite
		while True:
			try:
				data = self.sock.recv(19).decode("utf-8")
			except socket.timeout:
				self.printBox1("esperando nuevamente")
				continue
			except:
				# self.clients.remove(client_address)
				# self.printBox1("Se ha cerrado id={}, address={}".format(id, client_address))
				# self.updateListBox()
				print("FATAL")
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
				self.printBox1("Enviando resultado={} toAddress{}".format(result, (ipServer, puertoServer)))
				self.sock.sendall(str(result).encode("utf-8"))
			except:
				self.printBox1("Error id={}, address={}".format(id, (ipServer, puertoServer)))
				self.sock.sendall("Error".encode("utf-8"))
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