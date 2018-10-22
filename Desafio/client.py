#!/usr/bin/env python3
import pika
import threading
import operator
import sys
import tkinter as tkinter
import time
import threading
import pygame
import os

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
#audio = EasyID3("D:\\Programas e instaladores\\Libros y Pdf\\Arquitectura cliente servidor\\UTPArqClientServer\\Desafio\\songs\\The Magician-Dark Moor.mp3")
#audio["title"]="nombre de la song"


class rabbitmqClient:
	def __init__(self, ip="192.168.8.247"):
		#pygame - mixer control
		pygame.mixer.init(frequency=48000)
		#pygame.mixer.music.load('songs/The Magician-Dark Moor.mp3')
		self.songDuration = 0#MP3("songs/The Magician-Dark Moor.mp3").info.length
		#self.songDuration=pygame.mixer.Sound("Dark Moor   The Magician[1].mp3")
		#self.songDuration=self.durationSong.get_length()
		self.playing=False
		self.pause=False
		self.modified=False
		self.modifiedPercentage=0.0

		self.songListDictionary=self.updateDictionary("songs")
		
		#Tkinter
		self.root = tkinter.Tk()
		self.root.wm_title("playerACS")
		scrollbar = tkinter.Scrollbar(self.root, orient=tkinter.VERTICAL)
		self.textoBox = tkinter.Text(self.root, height=8, width=45, yscrollcommand=scrollbar.set)
		self.textoBox2 = tkinter.Text(self.root, height=8, width=45, yscrollcommand=scrollbar.set)
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
		#self.list.bind('<<ListboxActivate>>', self.listActive)
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

		# self.buttonUpdate.config(state=tkinter.DISABLED)

		
		

	def yview(self, *args):
		self.textoBox.yview(*args)
		self.textoBox2.yview(*args)
		self.list.yview(*args)

	def printBox1(self, value):
		self.textoBox.config(state=tkinter.NORMAL)
		self.textoBox.insert(tkinter.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.textoBox.see(tkinter.END)
		self.textoBox.config(state=tkinter.DISABLED)

	def printBox2(self, value):
		self.textoBox2.config(state=tkinter.NORMAL)
		self.textoBox2.insert(tkinter.END, "\n"+time.asctime(time.localtime(time.time()))+": "+str(value))
		self.textoBox2.see(tkinter.END)
		self.textoBox2.config(state=tkinter.DISABLED)
		"""
		self.textoBox2.config(state=tkinter.NORMAL)
		self.textoBox2.delete('1.0', tkinter.END)
		self.textoBox2.insert(tkinter.END, str(value))
		self.textoBox2.see(tkinter.END)
		self.textoBox2.config(state=tkinter.DISABLED)
		"""
		
	def updateListBox(self):
		self.list.delete(0, tkinter.END)#Borra TODO
		for song in self.songListDictionary:
			self.list.insert(tkinter.END, song)
		if(len(self.songListDictionary)>0):
			self.buttonPlayPause.config(state=tkinter.NORMAL)
			self.buttonStop.config(state=tkinter.NORMAL)

		#if(isinstance(item, list)):
		#	for i in item:
		#		self.list.insert(tkinter.END, i)
		#fileSelected=self.list.curselection()
		#if(len(fileSelected)==1):
		#	fileName=self.list.get(fileSelected[0])
		#	self.list.activate(fileSelected[0])
		#	self.list.configure(state=tkinter.DISABLED)
	def updateDictionary(self, folder):
		filesList=os.listdir(folder)
		songDictionary={}
		for fileName in filesList:
			"""
			try:
				audio = EasyID3(folder+"/"+fileName)
			except ID3NoHeaderError:
				audio = mutagen.File(folder+"/"+fileName, easy=True)
				audio.add_tags()
				audio.save()
			"""
			audio = EasyID3(folder+"/"+fileName)
			try:
				songDictionary[audio["title"]]=folder+"/"+fileName
			except:
				songDictionary[fileName.replace(".mp3", "")]=folder+"/"+fileName
		return songDictionary
		#audio["title"]="nombre de la song"

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
			self.list.activate(list(self.songListDictionary).index(self.stringSongName.get()))
		except:
			pass
		if(self.playing):
			if(not pygame.mixer.music.get_busy()):
				self.stringSongName.set(self.playerNext())
				pygame.mixer.music.load(self.songListDictionary.get(self.stringSongName.get()))
				pygame.mixer.music.play()
			

			self.progressBar.config(state=tkinter.NORMAL)
			self.progressBar.set((pygame.mixer.music.get_pos()/1000)/self.songDuration)
			self.stringStep.set(self.getMinuteSecond((pygame.mixer.music.get_pos()/1000)))
			self.progressBar.config(state=tkinter.DISABLED)
			# print("time length ", self.songDuration, type(self.songDuration))
			# print("time pos ", (pygame.mixer.music.get_pos()/1000), type((pygame.mixer.music.get_pos()/1000)))
			# print("newprogress ", (pygame.mixer.music.get_pos()/1000)/self.songDuration)
			
		else:
			if(pygame.mixer.music.get_busy()):
				pygame.mixer.music.pause()
		self.buttonPlayPause.after(50, self.player)
				

	def playerNext(self):
		playingActualSongIndex=list(self.songListDictionary).index(self.stringSongName.get())
		playingNextSongIndex=playingActualSongIndex+1
		if(playingNextSongIndex==len(self.songListDictionary)-1):
			playingNextSongIndex=0
		playingNextSongName=list(self.songListDictionary)[playingNextSongIndex]

		tempDict={}#separation
		tempDict[self.stringSongName.get()]=self.songListDictionary.pop(self.stringSongName.get())

		self.songListDictionary.update(tempDict)
		self.updateListBox()
		return playingNextSongName

	def playerOther(self, playingNextSongName):
		try:
			playingActualSongIndex=list(self.songListDictionary).index(self.stringSongName.get())
			tempDict={}#separation
			tempDict[self.stringSongName.get()]=self.songListDictionary.pop(self.stringSongName.get())
			self.songListDictionary.update(tempDict)
		except:
			pass
		
		tempDict={}#separation
		tempDict[playingNextSongName]=self.songListDictionary.pop(playingNextSongName)
		tempDict.update(self.songListDictionary)
		self.songListDictionary=tempDict.copy()
		self.updateListBox()
		return playingNextSongName


	#Can sock connection or sock
	def sendMessageMulti(self):
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
			self.channel.basic_publish(exchange='', routing_key="*",body=message)
			self.printBox2("Operación solicitada -> {}*{}".format(op1, op2))

	def runReceive(self):
		self.channel.start_consuming()

	def runGraph(self):
		self.buttonPlayPause.after(1000, self.player)
		self.root.mainloop()

	def receive(self, ch, method, properties, body):
		self.printBox2("resultado {}".format(body.decode("utf-8")))

if __name__ == '__main__':
	servidor=rabbitmqClient()
	print("Server iniciado")
	#hilo1=threading.Thread(target=servidor.runReceive)
	#hilo1.start()
	servidor.runGraph()