#!/usr/bin/env python3

import pika
import uuid

import threading
import os
import sys
import time

import tkinter as tkinter
import pygame

import mutagen
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# "album": "TALB",
# "composer": "TCOM",
# "genre": "TCON",
# "date": "TDRC",
# "lyricist": "TEXT",
# "title": "TIT2",
# "version": "TIT3",
# "artist": "TPE1",
# "tracknumber": "TRCK",

#mutagen.File("D:\\Programas e instaladores\\Libros y Pdf\\Arquitectura cliente servidor\\UTPArqClientServer\\Desafio\\songs\\Dark Moor   The Magician[1].mp3")["TIT2"].text
# (pygame.mixer.music.get_length() - pygame.mixer.music.get_pos())*-1

#from mutagen.easyid3 import EasyID3
#audio = EasyID3("D:\\Programas e instaladores\\Libros y Pdf\\Arquitectura cliente servidor\\UTPArqClientServer\\Desafio\\songs\\System Of A Down   BYOB (Video).mp3")
#audio["title"]="nombre de la song"


class rabbitmqClientSitio:
	def __init__(self, ip="localhost"):
		#rabbitmq
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip, socket_timeout=2))
		self.channel = self.connection.channel()
		#result=self.channel.queue_declare(queue="amqsitio1")
		result=self.channel.queue_declare(exclusive=True)#temporal queue
		self.queueNameMe = result.method.queue
		# self.channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)
		#self.channel.basic_cancel(consumer_tag)
		#self.channel.queue_delete(queue='name')
		print("mi cola ->", self.queueNameMe)
		self.channel.basic_consume(self.receive, queue=self.queueNameMe)

		self.queueNameService=None

		#pygame - mixer control
		pygame.mixer.init(frequency=44100)#set to 48000
		self.songDuration = 0
		self.playing=False
		self.pause=False
		self.modified=False
		self.modifiedPercentage=0.0
		self.folders=["songs"]
		self.songListDictionary={}
		self.songListNew=False
		self.songList=list(self.songListDictionary)
		
		#Tkinter
		self.root = tkinter.Tk()
		self.root.wm_title("player Sitio")
		scrollbar = tkinter.Scrollbar(self.root, orient=tkinter.VERTICAL)
		self.textoBox = tkinter.Text(self.root, height=8, width=60, yscrollcommand=scrollbar.set)
		self.textoBox2 = tkinter.Text(self.root, height=8, width=60, yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.yview)
		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		
		self.textoBox.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.textoBox.config(state=tkinter.DISABLED)
		self.textoBox2.pack(side=tkinter.LEFT, fill=tkinter.Y)
		self.textoBox2.config(state=tkinter.NORMAL)
		frame = tkinter.Frame(self.root)
		frame.pack()

		#list
		self.list = tkinter.Listbox(self.root, width=30, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set, exportselection=False)
		self.list.bind('<<ListboxSelect>>', self.showInfoSong)
		self.list.pack(fill=tkinter.BOTH, expand=1)

		# self.command = tkinter.StringVar()
		# tkinter.Entry(frame, textvariable=self.command).grid(row=1, column=1)
		tkinter.Label(frame, text='State:').grid(row=0, column=0)
		self.answer = tkinter.StringVar()
		self.answer.set("Stoped")
		tkinter.Label(frame, textvariable=self.answer).grid(row=0, column=1)

		tkinter.Label(frame, text='Song:').grid(row=1, column=0)
		self.stringSongName = tkinter.StringVar()
		self.stringSongName.set("")
		tkinter.Label(frame, textvariable=self.stringSongName).grid(row=1, column=1)

		tkinter.Label(frame, text='Playing:').grid(row=2, column=0)
		self.progressBar = tkinter.Scale(frame, from_=0.00, to=1.00, orient=tkinter.HORIZONTAL, digits=3, resolution=0.01, state=tkinter.DISABLED, showvalue=0)
		self.progressBar.grid(row=2, column=1, columnspan=1)

		tkinter.Label(frame, text='Duration:').grid(row=3, column=0)
		self.stringDuration = tkinter.StringVar()
		self.stringDuration.set(self.getMinuteSecond(self.songDuration))
		tkinter.Label(frame, textvariable=self.stringDuration).grid(row=3, column=1)

		tkinter.Label(frame, text='TimeStep:').grid(row=4, column=0)
		self.stringStep = tkinter.StringVar()
		self.stringStep.set(0)
		tkinter.Label(frame, textvariable=self.stringStep).grid(row=4, column=1)

		self.stringPlayPause = tkinter.StringVar()
		self.stringPlayPause.set("►")
		self.buttonPlayPause = tkinter.Button(frame, textvariable=self.stringPlayPause, command=self.playerPlayPause, state=tkinter.DISABLED)
		self.buttonPlayPause.grid(row=5, column=0, columnspan=1)

		self.stringStop = tkinter.StringVar()
		self.stringStop.set("■")
		self.buttonStop = tkinter.Button(frame, textvariable=self.stringStop, command=self.playerStop, state=tkinter.DISABLED)
		self.buttonStop.grid(row=5, column=1, columnspan=1)

		self.buttonUpdate = tkinter.Button(frame, text='Update List', command=self.updateListBox)
		self.buttonUpdate.grid(row=6, column=0, columnspan=1)

		self.buttonSetMeta = tkinter.Button(frame, text='Set metadata', command=self.setMeta)
		self.buttonSetMeta.grid(row=6, column=1, columnspan=1)

		self.buttonUpdateAll = tkinter.Button(frame, text='Update All Files', command=self.updateAll)
		self.buttonUpdateAll.grid(row=7, column=0, columnspan=1)

		# self.buttonUpdate.config(state=tkinter.DISABLED)

		
		

	def yview(self, *args):
		self.textoBox.yview(*args)
		self.textoBox2.yview(*args)
		self.list.yview(*args)

	def printBox1(self, value):
		self.textoBox.config(state=tkinter.NORMAL)
		self.textoBox.insert(tkinter.END, "\n"+time.asctime(time.localtime(time.perf_counter()))+": "+str(value))
		self.textoBox.see(tkinter.END)
		self.textoBox.config(state=tkinter.DISABLED)

	def printBox2(self, value):
		#self.textoBox2.config(state=tkinter.NORMAL)
		self.textoBox2.delete('1.0', tkinter.END)
		if(self.queueNameService is not None):
			self.textoBox2.insert(tkinter.END, str("Codigo: "+self.queueNameService+"\n"))
		else:
			self.textoBox2.insert(tkinter.END, str("Codigo: No Code"+"\n"))
		self.textoBox2.insert(tkinter.END, str(value))
		self.textoBox2.see(tkinter.END)
		#self.textoBox2.config(state=tkinter.DISABLED)
		
	def updateListOrder(self):
		newList=[]
		maxValue=0
		for song in self.songVotesDictionary:
			valueIn=self.songVotesDictionary.get(song)
			if(valueIn > maxValue):
				maxValue=valueIn=0
		newList.append(self.songList[0])
		self.songVotesDictionary.pop(self.songList[0])
		while len(self.songVotesDictionary)!=0:
			newMax=0
			
			for song in self.songlist:
				if(song in self.songVotesDictionary):
					valueIn=self.songVotesDictionary.get(song)
				else:
					continue
				if(valueIn==maxValue):
					newList.append(song)
					self.songVotesDictionary.pop(song)
				elif(valueIn>newMax):
					newMax=valueIn
			maxValue=newMax
		return newList
			




	def updateListBox(self):
		self.list.delete(0, tkinter.END)#Borra TODO
		sendList=[]
		for song in self.songList:
			if(self.queueNameService is not None):
				sendList.append({song:self.getInfoSong(song)})
			self.list.insert(tkinter.END, song)
		if(len(self.songList)>0):
			self.buttonPlayPause.config(state=tkinter.NORMAL)
			self.buttonStop.config(state=tkinter.NORMAL)
		

			

	def updateAll(self):
		self.songListDictionary={}
		sendList=[]
		for folder in self.folders:
			self.songListDictionary.update(self.updateDictionary(folder))
		self.songList=list(self.songListDictionary)
		
		for song in self.songList:
			if(self.queueNameService is not None):
				sendList.append({song:self.getInfoSong(song)})
		if(self.queueNameService is not None):
			self.channel.basic_publish(exchange='', routing_key=self.queueNameService, body="listaInicial`"+str(sendList), properties=pika.BasicProperties(
							delivery_mode = 2, # make message persistent, not end until message consumes
						))
		
		self.updateListBox()
		self.printBox1("Se ha actualizado la lista de archivos")

	def updateDictionary(self, folder):
		filesList=os.listdir(folder)
		songDictionary={}
		for fileName in filesList:
			if(os.path.isdir(fileName)):
				songDictionary.update(self.updateDictionary(folder+"/"+fileName))
			if(not ".mp3" in fileName):
				continue
			try:
				audio = EasyID3(folder+"/"+fileName)
			except ID3NoHeaderError:
				audio = mutagen.File(folder+"/"+fileName, easy=True)
				audio.add_tags()
				audio.save()

			audio = EasyID3(folder+"/"+fileName)
			try:
				audio["title"]
			except:
				audio["title"]=""
				audio.save()
			
			if(len(audio["title"][0])>0):
				if(str(audio["title"]).replace("[", "").replace("'", "").replace("]", "") in songDictionary):
					songDictionary[str(audio["title"]).replace("[", "").replace("'", "").replace("]", "")+"*"]=folder+"/"+fileName
				else:
					songDictionary[str(audio["title"]).replace("[", "").replace("'", "").replace("]", "")]=folder+"/"+fileName
			else:
				if(fileName.replace(".mp3", "") in songDictionary):
					songDictionary[fileName.replace(".mp3", "")+"*"]=folder+"/"+fileName
				else:
					songDictionary[fileName.replace(".mp3", "")]=folder+"/"+fileName
		return songDictionary

	def updateListFromServer(self):
		if(self.queueNameService is not None):
			# Try here
			self.songListNew=False
			self.channel.basic_publish(exchange='', routing_key=self.queueNameService, body="listaActualizada`None", properties=pika.BasicProperties(
							delivery_mode = 2, # make message persistent, not end until message consumes
						))
			startTime = time.perf_counter()
			#while not self.songListNew:
			#	self.connection.process_data_events()
			#	elapsed = time.perf_counter() - startTime
			#	if(elapsed>0.5):
			#		break
			# self.songList=self.updateListOrder()############
			self.printBox1("Se ha actualizado la lista del servidor")
			self.updateListBox()
		self.buttonUpdateAll.after(20000, self.updateListFromServer)

	
	def getInfoSong(self, songName):
		dataResult={"title":"", "artist":"" , "album":"", "genre":"", "tracknumber":"", "version":"", "date":"", "composer":"", "lyricist":""}
		audio = EasyID3(self.songListDictionary.get(songName))
		
		for metaInfo in dataResult:
			if(metaInfo in audio):
				dataResult[metaInfo]=str(audio[metaInfo])	
			else:
				continue
		audio = MP3(self.songListDictionary.get(songName))
		dataResult["duration"]=[self.getMinuteSecond(audio.info.length)]
		return dataResult
		
		

	def showInfoSong(self,event):
		listWigget=event.widget
		songSelected=listWigget.curselection()
		songName=None
		if(len(songSelected)==1):
			songName=listWigget.get(songSelected[0])
		if(songName is not None):
			dataString=""
			audio = EasyID3(self.songListDictionary.get(songName))
			metadataDict={"title":"Titulo: ", "artist":"Artista: " , "album":"Album: ", "genre":"Género: ", "tracknumber":"Número de pista: ", "version":"Versión: ", "date":"Año: ", "composer":"Compositor: ", "lyricist":"Escritor: "}
			
			for metaInfo in metadataDict:
				dataString+=metadataDict.get(metaInfo)
				if(metaInfo in audio):
					dataString+=str(audio[metaInfo])+"\n"	
				else:
					dataString+="\n"	

			dataString+="\n"
			audio = MP3(self.songListDictionary.get(songName))
			dataString+="Duración: "+self.getMinuteSecond(audio.info.length)+"\n"
			dataString+="Bitrate: "+str(audio.info.bitrate)+"\n"
			dataString+="Frecuencia: {}Hz".format(str(audio.info.sample_rate))+"\n"
			self.printBox2(dataString.replace("[", "").replace("'", "").replace("]", ""))
			

			# print("audio -<\n ", sendDict)
			
	def setMeta(self):
		songSelected=self.list.curselection()
		songName=None
		if(len(songSelected)==1):
			songName=self.list.get(songSelected[0])
		if(songName is not None):
			# dataString=""
			audio=EasyID3(self.songListDictionary.get(songName))
			
			data=self.textoBox2.get("1.0", tkinter.END).split("\n")
			title, artists, audio["album"], audio["genre"], audio["tracknumber"], audio["version"], audio["date"], audio["composer"], audio["lyricist"]=data[1:9]

			metaDataDict={"title":8, "artist":9, "album":7, "genre":8, "tracknumber":17, "version":9, "date":5, "composer":12, "lyricist":10}
			for enum, metaInfo in enumerate(metaDataDict):
				if(", " in data[enum]):
					for indexInfo, info in enumerate(data[enum][metaDataDict.get(metaInfo):].split(", ")):
						if(indexInfo==0):
							audio[metaInfo]=info
						else:
							values=audio[metaInfo]
							values.append(info)
							audio[metaInfo]=values
				else:
					audio[metaInfo]=data[enum][metaDataDict.get(metaInfo):]
			audio.save()
			self.printBox1("Se ha actualizado metadata de la canción {}".format(songName))
			
			

			

			# self.textoBox2

	def getMinuteSecond(self, value):
		seconds=int(value%60)
		minutes=int(value/60)
		return str(minutes)+":"+str(seconds)

	def playerPlayPause(self):
		self.playing=not self.playing
		if(self.playing):	
			self.stringPlayPause.set("❚❚")
			self.answer.set("playing")
			songSelected=self.list.curselection()
			songName=None
			if(len(songSelected)==1):
				songName=self.list.get(songSelected[0])
				self.list.activate(songSelected[0])
			if(songName is not None):
				if(songName!=self.stringSongName.get()):
					self.playerOther(songName)
					if(self.queueNameService is not None):
						# Try here
						self.songListNew=False

						self.channel.basic_publish(exchange='', routing_key=self.queueNameService, body="otro`None", properties=pika.BasicProperties(
							delivery_mode = 2, # make message persistent, not end until message consumes
						))
						startTime = time.perf_counter()
						#while not self.songListNew:
						#	self.connection.process_data_events()
						#	elapsed = time.perf_counter() - startTime
						#	if(elapsed>0.5):
						#		print("TIME OUT")
						#		break
						# self.songList=self.updateListOrder()############
						self.updateListBox()
					
					# print("hice other")
					self.stringSongName.set(songName)
					pygame.mixer.music.load(self.songListDictionary.get(songName))
					self.songDuration = MP3(self.songListDictionary.get(songName)).info.length
					self.stringDuration.set(self.getMinuteSecond(self.songDuration))
					pygame.mixer.music.play()
			if(pygame.mixer.music.get_busy()):
				pygame.mixer.music.unpause()
			else:
				pygame.mixer.music.play()
		else:
			self.stringPlayPause.set("►")
			self.answer.set("paused")
			if(pygame.mixer.music.get_busy()):
				pygame.mixer.music.pause()
	
	def playerStop(self):
		self.playing=False
		self.stringPlayPause.set("►")
		self.answer.set("Stoped")
		if(pygame.mixer.music.get_busy()):
			pygame.mixer.music.stop()
			
	
	def player(self):
		try:
			self.list.activate(self.songList.index(self.stringSongName.get()))
		except:
			pass
		if(self.playing):
			if(not pygame.mixer.music.get_busy()):
				songActual=self.songList[0]
				if(self.queueNameService is not None):
					print("oe use siguiente")
					self.songListNew=False
					self.channel.basic_publish(exchange='', routing_key=self.queueNameService, body="terminoCancion`None", properties=pika.BasicProperties(
							delivery_mode = 2, # make message persistent, not end until message consumes
						))
					startTime = time.perf_counter()
					elapsed=0
					while(elapsed<1):
						elapsed = time.perf_counter() - startTime
						continue
					#while not self.songListNew:
					#	self.connection.process_data_events()
						
					
					#	elapsed = time.perf_counter() - startTime
					#	if(elapsed>1):
					#		print("TIME OUT")
					#		break
					
					# self.songList=self.updateListOrder()############
				else:
					self.stringSongName.set(self.playerNext(songActual))
					self.songDuration = MP3(self.songListDictionary.get(self.stringSongName.get())).info.length
					self.stringDuration.set(self.getMinuteSecond(self.songDuration))
					pygame.mixer.music.load(self.songListDictionary.get(self.stringSongName.get()))
					pygame.mixer.music.play()
			
			self.progressBar.config(state=tkinter.NORMAL)
			self.progressBar.set((pygame.mixer.music.get_pos()/1000)/self.songDuration)
			self.stringStep.set(self.getMinuteSecond((pygame.mixer.music.get_pos()/1000)))
			self.progressBar.config(state=tkinter.DISABLED)
			
		else:
			if(pygame.mixer.music.get_busy()):
				pygame.mixer.music.pause()
		self.buttonPlayPause.after(50, self.player)
				

	def playerNext(self, actualSong):
		self.songList.remove(actualSong)
		self.songList.append(actualSong)
		self.updateListBox()
		return self.songList[0]

	def playerOther(self, playingNextSongName):
		playingActualSongName=self.songList.pop(0)
		self.songList.append(playingActualSongName)

		playingNextSongIndex=self.songList.index(playingNextSongName)
		playingNextSongName=self.songList.pop(playingNextSongIndex)
		self.songList.insert(0, playingNextSongName)
		# print("new list", self.songList)
		self.updateListBox()


	#Can sock connection or sock
	def connectReceive(self):
		self.printBox1("connectando al servicio del medio")
		self.channel.basic_publish(exchange='', routing_key="conectoSitio", body=self.queueNameMe, properties=pika.BasicProperties(
							delivery_mode = 2, # make message persistent, not end until message consumes
						))




	def receive(self, ch, method, properties, body):
		body=body.decode("utf-8")
		print("se ha recibido ->", body)
		self.printBox1("mensaje recibido {}".format(body))
		if(self.queueNameService is None):
			self.queueNameService=body
			self.printBox2("")
			self.printBox1("se ha conectado al servicio del medio")
		else:
			# self.songVotesDictionary=eval(body)
			
			self.songList=eval(body)
			print("se ha recibido la lista -> ", self.songList)
			self.stringSongName.set(self.songList[0])
			
			self.songDuration = MP3(self.songListDictionary.get(self.stringSongName.get())).info.length
			self.stringDuration.set(self.getMinuteSecond(self.songDuration))
			pygame.mixer.music.load(self.songListDictionary.get(self.stringSongName.get()))
			pygame.mixer.music.play()
			self.songListNew=True
			self.updateListBox()
		ch.basic_ack(delivery_tag = method.delivery_tag)

	
	def runReceive(self):
		self.channel.start_consuming()

	def runGraph(self):
		self.buttonPlayPause.after(1000, self.player)
		self.buttonUpdate.after(1000, self.connectReceive)
		#self.buttonUpdateAll.after(20000, self.updateListFromServer)
		self.root.mainloop()

	

if __name__ == '__main__':
	servidor=rabbitmqClientSitio("www.nidal.online")
	hilo1=threading.Thread(target=servidor.runReceive)
	hilo1.start()

	print("Server iniciado")
	servidor.runGraph()
	os._exit(1)# kill main thread