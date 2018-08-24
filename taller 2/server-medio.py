import threading
import socket
import operator
import sys
import tkinter as tk
import time

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
		self.sock.settimeout(1)#Establecer tiempo limite de espera en segundos por cada recvfrom
		self.clients={}
		self.servers={}
		self.idIterator=0
		self.waitMore=False

		#tk
		self.root = tk.Tk()
		self.root.wm_title("calculo-server-Middleware")
		scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
		self.TextoBox = tk.Text(self.root, height=8, width=80, yscrollcommand=scrollbar.set)
		self.TextoBox2 = tk.Text(self.root, height=8, width=80, yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.yview)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		
		self.TextoBox.pack(side=tk.LEFT, fill=tk.Y)
		self.TextoBox.config(state=tk.DISABLED)
		self.TextoBox2.pack(side=tk.LEFT, fill=tk.Y)
		self.TextoBox2.config(state=tk.DISABLED)
		frame = tk.Frame(self.root)
		frame.pack()


		listClientsTitle=tk.Label(self.root,text="Clientes")
		listClientsTitle.pack(fill=tk.BOTH, expand=1)

		self.listClients = tk.Listbox(self.root, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
		self.listClients.pack(fill=tk.BOTH, expand=1)
		
		listServersTitle=tk.Label(self.root,text="Servidores")
		listServersTitle.pack(fill=tk.BOTH, expand=1)

		self.listServers = tk.Listbox(self.root, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
		self.listServers.pack(fill=tk.BOTH, expand=1)


		self.buttonWaitNew = tk.Button(frame, text='Start Wait new', command=self.toggleWaitNew)
		self.buttonWaitNew.grid(row=2, columnspan=1)

		self.buttonUpdateClients = tk.Button(frame, text='Update List Clients', command=self.updateListBoxClients)
		self.buttonUpdateClients.grid(row=3, columnspan=1)

		self.buttonUpdateServers = tk.Button(frame, text='Update List Servers', command=self.updateListBoxClients)
		self.buttonUpdateServers.grid(row=4, columnspan=1)

		# self.buttonUpdate.config(state=tk.DISABLED)

		tk.Label(frame, text='Estado').grid(row=1, column=0)
		self.answer = tk.StringVar()
		self.answer.set("Ready")
		tk.Label(frame, textvariable=self.answer).grid(row=1, column=1)

	def yview(self, *args):
		self.TextoBox.yview(*args)
		self.TextoBox2.yview(*args)
		self.listClients.yview(*args)
		self.listServers.yview(*args)

	def printBox1(self, value):
		self.TextoBox.config(state=tk.NORMAL)
		self.TextoBox.insert(tk.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.TextoBox.see(tk.END)
		self.TextoBox.config(state=tk.DISABLED)

	def printBox2(self, value):
		self.TextoBox2.config(state=tk.NORMAL)
		self.TextoBox2.insert(tk.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.TextoBox2.see(tk.END)
		self.TextoBox2.config(state=tk.DISABLED)


	def updateListBoxClients(self):
		self.printBox1("Actualizando lista de clientes")
		self.listClients.selection_clear(0, tk.END)
		listaTemp=self.clients
		self.listClients.delete(0, tk.END)#Borra TODO
		for i in listaTemp:
			self.listClients.insert(tk.END, i+" <-> "+str(listaTemp[i]["address"]))

	def updateListBoxServers(self):
		self.printBox1("Actualizando lista de servidores")
		self.listServers.selection_clear(0, tk.END)
		listaTemp=self.servers
		self.listServers.delete(0, tk.END)#Borra TODO
		for i in listaTemp:
			self.listServers.insert(tk.END, i+" <-> "+str(listaTemp[i]["address"]))

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
		try:
			sock.close()
		except:
			print("No se puede cerrar")
		return None
	

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
		try:
			sock.close()
		except:
			print("No se puede cerrar")
		return None

	def toggleWaitNew(self):
		self.waitMore=not self.waitMore
		if(self.waitMore):
			self.waitNew()
			
	def waitNew(self):
		self.printBox1("Creando nueva conexion")
		hilo1=threading.Thread(target=self.runConecction, args=([self.idIterator]))
		self.idIterator+=1
		hilo1.start()
		if(self.waitMore):
			self.buttonWaitNew["text"]="End Wait new"
			self.buttonWaitNew.after(1000, self.waitNew)
		else:
			self.buttonWaitNew["text"]="Start Wait new"

	def runConecction(self, id):
		whoIs=None
		self.printBox1("Esperando conexión, id={}".format(id))
		self.answer.set("Waiting conecction")
		while True:
			try:
				connection, client_address = self.sock.accept()
				self.printBox1("conexión lista -> conecction {} addres {}".format(connection, client_address))
				self.sendMsg(str(id), connection, to=str(client_address))
				self.answer.set("Connected")
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
		self.answer.set("Wait who is")
		try:
			whoIs = self.recvMsg(connection, to=str(client_address))
			if(whoIs=="cliente"):
				whoIs+="-"+str(id)
				self.clients[whoIs]={"connection":connection, "address":client_address}
				self.answer.set("Setting client")
			
		except socket.timeout:
			self.printBox1("cerrada id={}".format(id))
			return
		except:
			self.printBox1("Cerrado id={}".format(id))
			return
		self.updateListBoxClients()
		# Recibe los datos en trozos y reetransmite
		if whoIs[:7]!="cliente":
			self.answer.set("is Service")
			self.sendMsg(str(client_address[0]), connection, to=str(client_address))
			#try:
			data = self.recvMsg(connection, to=str(client_address))#esperando puerto
			sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((client_address[0], int(data)))
			self.servers[whoIs]={"connection":sock, "address":(client_address[0], int(data))}

			connection.close()
			# self.clients.pop(whoIs)
			self.updateListBoxClients()
			self.updateListBoxServers()
			self.answer.set("Ready")
			#except:
		
		self.answer.set("Ready")
		if whoIs[:7]=="cliente":
			self.runClientThread(connection, client_address, whoIs)

	def runClientThread(self, connection, client_address, whoIs):
		hilo1=threading.Thread(target=self.runClientConnect, args=([connection, client_address, whoIs]))
		hilo1.start()

	def runClientConnect(self, connection, client_address, whoIs):
		data = self.recvMsg(connection, to=str(client_address))
		if(data is None):
			self.clients.pop(whoIs)
			print("cliente muere", client_address)
			self.printBox1("Se ha cerrado, address={}".format(client_address))
			self.updateListBoxClients()
			return
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
			self.sendMsg("Bad format", connection, to=str(client_address))

		if(correctFormat):
			op, op1, op2=str(data).split(",")
			self.printBox2("operacion {} {} {}".format(op1, op, op2))
			# print(self.servers)
			try:
				self.sendMsg(data, self.servers.get(op).get("connection"), to=str(self.servers.get(op).get("address")))
				result=self.recvMsg(self.servers.get(op).get("connection"), to=str(self.servers.get(op).get("address")))
			except:
				result=False
			if(result is None):
				self.printBox1("Se ha cerrado operator={}, address={}".format(op, self.servers.get(op).get("address")))
				self.servers.pop(op)
				result="Caido"
				self.updateListBoxClients()
			elif(not result):
				self.printBox1("No se tiene servidor tipo={}".format(op))
				result="No se registra servidor"
			self.printBox2("resultado -> {}".format(result))
			self.sendMsg(result, connection, to=str(client_address))
			self.buttonUpdateClients.after(1000, self.runClientThread, connection, client_address, whoIs)

	
		
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