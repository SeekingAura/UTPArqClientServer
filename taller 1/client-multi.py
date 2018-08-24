import socket
import tkinter as tkinter
import time

class TCPSocketClient:
	def __init__(self, ip, puerto):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # UDP
		self.ip=ip
		self.puerto=puerto
		self.sock.settimeout(30)#tiempo de espera para que conecte
		self.wm_title="calculo-cliente"
		# self.clients=[]

		#Tkinter
		self.root = tkinter.Tk()
		self.root.wm_title(self.wm_title)
		scrollbar = tkinter.Scrollbar(self.root, orient=tkinter.VERTICAL)
		self.TextoBox = tkinter.Text(self.root, height=8, width=80, yscrollcommand=scrollbar.set)
		self.TextoBox2 = tkinter.Text(self.root, height=8, width=80, yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.yview)
		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		
		self.TextoBox.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.TextoBox.config(state=tkinter.DISABLED)
		self.TextoBox2.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.TextoBox2.config(state=tkinter.DISABLED)
		self.command = tkinter.StringVar()
		
		frame = tkinter.Frame(self.root)
		frame.pack()

		tkinter.Entry(frame, textvariable=self.command).grid(row=2, column=1)
		#self.command.get()
		#self.command.set("")
		self.buttonShowFile = tkinter.Button(frame, text='Send message', command=self.sendMessage)
		self.buttonShowFile.grid(row=2, columnspan=1)

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

	def runClient(self):
		self.sock.connect((self.ip, self.puerto))
		try:
			data = self.sock.recv(19).decode("utf-8")
			self.wm_title+=" - "+data
			self.root.wm_title(self.wm_title)
			self.sock.sendall("cliente".encode("utf-8"))
		except:
			print("Failed conecction")
			return
		self.runGraph()
	def sendMessage(self):
		message=self.command.get()
		self.command.set("")
		self.printBox1("Enviando -> {}".format(message))
		self.sock.sendall(message.encode("utf-8"))
		try:
			operator, operator1, operator2=message.split(",")
			self.printBox2("Operación -> {}{}{}".format(operator1, operator, operator2))
		except:
			self.printBox2("Bad Syntax")
		try:
			data = self.sock.recv(19).decode("utf-8")
			self.printBox1("recibido -> {}".format(data))
		except:
			self.printBox1("Tiempo de espera superado")
			data="error"
		
		
		self.printBox2("resultado -> {}".format(data))
		
	
	def runGraph(self):
		self.root.mainloop()

if __name__ == '__main__':
	ipServer = input("Ingrese la ip del server -> ")
	puertoServer = int(input("ingrese el puerto del server -> "))
	print("server IP:", ipServer)
	print("server port:", puertoServer)
	cliente=TCPSocketClient(ipServer, puertoServer)
	cliente.runClient()