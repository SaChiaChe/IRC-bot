# -*- coding: UTF-8 -*-
import socket, select

DailyHoroscopes = ["今天在你的專業領域上會有好機會降臨", "今天可能會有金錢上的損失", 	"今天會遇到比較固執又難以溝通的長輩", "今天會遇到脾氣很差的人", "今天麻煩事一樁接著一樁", "今天有升官的機會", "今天適合處理金錢相關的事情", "今天嚴謹的態度是致勝的關鍵", "今天會遇到想法、脾氣瞬息萬變的女性長輩", "今天在工作中會遇到不同調、不合拍的類型", "今天容易說錯話", "今天效率是帶來幸運的關鍵"]
Constellations = ["capricorn", "aquarius", "pisces", "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius"]

def SendMsg(Socket, Message):
	Socket.send(bytes(Message + "\r\n", encoding = "utf-8"))
	return

def SendPRIVMSG(Socket, Receiver, Message):
	SendMsg(Socket, "PRIVMSG " + Receiver + " :" + Message)
	return

def PRIVMSGHandler(Msg):
	MsgSplit = Msg.split(":")
	GotMsg = MsgSplit[-1].strip("\r\n").strip()
	Sender = MsgSplit[1].split("!")[0].strip()
	Receiver = MsgSplit[-2].strip().split()[-1].strip()
	return [GotMsg, Sender, Receiver]

def NonBlockingStdin(Port):
	import socket
	StdinSocket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	StdinSocket_.bind((socket.gethostname() , Port))
	StdinSocket_.listen(1)
	End = False
	while not End:
		Client, Address = StdinSocket_.accept()
		while not End:
			STDIN = input()
			if STDIN == "QUIT":
				Client.send(bytes(STDIN, encoding = "utf-8"))
				End == True
				return
			Client.send(bytes(STDIN, encoding = "utf-8"))
	return

def CreateStdinThread():
	from random import randint
	from threading import Thread

	global StdinThread
	global Port
	ThreadCreated = False
	while not ThreadCreated:
		try:
			Port = randint(111, 65535)
			StdinThread = Thread(target = NonBlockingStdin, args = [Port])
			print("==========Stdin Thread Created==========")
			StdinThread.start()
			ThreadCreated = True
			break
		except:
			print("Failed to create thread, try again")
			continue
	return 

def ConnectStdin():
	StdinConn = False
	while not StdinConn:
		try:
			StdinSocket.connect((socket.gethostname() , Port))
			StdinConn = True
			print("==========Connected to Stdin Thread==========")
			break
		except socket.error as e:
			# print(e)
			print("Failed to connect stdin, try again")
			continue
	return

def ServerShutDown():
	print("Connection lost")
	global Connected
	Connected = False
	return

def PINGHandler(IRCSocket, IRCMsg):
	# SendMsg(IRCSocket, "PONG")
	return

def TaskB(IRCSocket, Sender, Msg):
	def DailyHoroscope(Constellation):
		global DailyHoroscopes
		global Constellations
		Id = Constellations.index(Constellation.lower())
		return DailyHoroscopes[Id]

	ReplyMsg = DailyHoroscope(Msg)
	SendPRIVMSG(IRCSocket, Sender, ReplyMsg)
	print("Send: ", ReplyMsg.strip("\r\n"))
	return

def TaskC(IRCSocket, Sender):
	from random import randint

	Player = Sender
	TargetNum = randint(1, 10)
	print("Try to guess ", TargetNum)
	SendPRIVMSG(IRCSocket, Sender, "猜一個1~10之間的數字!")
	Success = False
	GuessRange = range(1, 11)
	while(not Success):
		Msg = IRCSocket.recv(4096).decode().strip("\r\n")
		print(Msg)

		#Server shut down
		if Msg == "":
			ServerShutDown()
			return

		#PING
		if IRCMsg.find("PING ") != -1:
			PINGHandler(IRCSocket, Msg)
			continue

		GotMsg, Sender, Receiver = PRIVMSGHandler(Msg)

		#Player disconnected from the server
		if IRCMsg.find("QUIT Connection lost") != -1 and Sender == Player:
			print("Player QUIT, end game")
			return

		#Not sent to me
		global Nickname
		if Receiver != Nickname:
			print("Not PRIVMSG to me")
			continue

		#Not current player
		if Player != Sender:
			print("Not Current player")
			continue

		#Test if the player guessed an integer
		try:
			GuessNum = int(GotMsg)
		except ValueError:
			print("Msg is not a integer!")
			continue

		#Check if player guessed out of 1~10
		if GuessNum not in range(1, 11):
			print("Illegal guess")
			continue
		#The guessed number is not ensured legal
		else:
			#Check the if the guessed number is in the logical correct range
			if GuessNum not in GuessRange:
				if GuessNum < min(GuessRange):
					ReplyMsg = "都說過大於" + str(min(GuessRange)-1) + "了 =_="
					SendPRIVMSG(IRCSocket, Sender, ReplyMsg)
					print("Send: ", ReplyMsg.strip("\r\n"))
					continue
				elif GuessNum > max(GuessRange):
					ReplyMsg = "都說過小於" + str(max(GuessRange)+1) + "了 =_="
					SendPRIVMSG(IRCSocket, Sender, ReplyMsg)
					print("Send: ", ReplyMsg.strip("\r\n"))
					continue
			#The guessed number is too small
			if GuessNum < TargetNum:
				GuessRange = range(GuessNum+1, max(GuessRange)+1)
				ReplyMsg = "大於" + str(GuessNum) + "!"
				SendPRIVMSG(IRCSocket, Sender, ReplyMsg)
				print("Send: ", ReplyMsg.strip("\r\n"))
				continue
			#The guessed number is too big
			elif GuessNum > TargetNum:
				GuessRange = range(min(GuessRange), GuessNum)
				ReplyMsg = "小於" + str(GuessNum) + "!"
				SendPRIVMSG(IRCSocket, Sender, ReplyMsg)
				print("Send: ", ReplyMsg.strip("\r\n"))
				continue
			#Correct!!!
			else:
				GuessRange = [GuessNum]
				ReplyMsg = "正確答案為" + str(TargetNum) + "! 恭喜猜中"
				SendPRIVMSG(IRCSocket, Sender, ReplyMsg)
				print("Send: ", ReplyMsg.strip("\r\n"))
				Success = True
				continue

def TaskD(IRCSocket, Sender, Msg):
	def SongTitleEncoder(Title):
		from urllib.parse import quote
		from string import printable as printable

		#Split the title
		TitleList = Title.split()
		#Concatenate the song title split with '+'
		CatTitle = TitleList[0]
		for i in range(1, len(TitleList)):
			CatTitle += "+" + TitleList[i]
		#Encode the song title
		EncodedTitle = quote(CatTitle, safe = printable)
		return EncodedTitle

	def Musicbot(Title):
		from bs4 import BeautifulSoup
		from urllib.request import urlopen

		Url = "https://www.youtube.com/results?search_query=" + Title
		search_result = urlopen(Url)
		soup = BeautifulSoup(search_result, "html.parser")
		ResultItem = soup.findAll('a', {"class": "yt-uix-tile-link"})

		Found = False
		ID = 0
		while not Found:
			FirstVideo = str(ResultItem[ID]).split()
			RequestLink = "https://www.youtube.com"
			for attr in FirstVideo:
				if attr.find("/watch?v=") != -1:
					RequestLink += attr.strip("href=").strip("\"\"")
					Found = True
					break
			ID += 1

		return RequestLink

	#Song title missing
	if len(Msg.split()) < 2:
		print("Song Title Missing")
		return

	#Get the song title
	SongTitle = Msg.split(" ", 1)[1]
	print("Search for: ", SongTitle)

	#First encode the title (for chinese characters)
	TargetSong = SongTitleEncoder(SongTitle)

	#Start web crawling
	FoundUrl = Musicbot(TargetSong)

	SendPRIVMSG(IRCSocket, Sender, FoundUrl)
	print("Send: ", FoundUrl.strip("\r\n"))
	return

def TaskE(IRCSocket, Sender):
	Player = Sender
	ChatReadList = [IRCSocket, StdinSocket]
	print("==========", Player, "想跟你聯繫==========")
	ChatEnd = False
	while not ChatEnd:
		ChatRl, ChatWl, ChatError = select.select(ChatReadList, [], [])
		for fd in ChatRl:
			if fd is IRCSocket:
				Msg = IRCSocket.recv(4096).decode().strip("\r\n")
				# print(Msg)

				#Server shut down
				if Msg == "":
					ServerShutDown()
					return

				#PING
				if IRCMsg.find("PING ") != -1:
					PINGHandler(IRCSocket, Msg)
					continue

				GotMsg, Sender, Receiver = PRIVMSGHandler(Msg)

				#Player disconnected from the server
				if IRCMsg.find("QUIT Connection lost") != -1 and Sender == Player:
					print("Player QUIT, end chat")
					return

				#Not sent to me
				global Nickname
				if Receiver != Nickname:
					# print("Not PRIVMSG to me")
					continue

				#Not current player
				if Player != Sender:
					# print("Not Current player")
					continue

				#Legal message, display it
				print(Player + "：" + GotMsg)

				#Player ended chat
				if GotMsg == "!bye":
					ChatEnd = True
					break

			if fd is StdinSocket:
				StdinMsg = StdinSocket.recv(4096).decode().strip("\r\n")

				#Stdin socket disconnected
				if StdinMsg == "":
					print("Stdin connection lost")
					ChatEnd = True
					break

				#Send PRIVMSG
				SendPRIVMSG(IRCSocket, Player, StdinMsg)

	#Chat end
	print("==========", Player, "已離開聊天室==========")
	return

def IRCMsgHandler(IRCSocket, Message):
	#Server shut down
	if Message == "":
		ServerShutDown()
		return

	#PING
	if IRCMsg.find("PING ") != -1:
		PINGHandler(IRCSocket, Message)
		return

	#Get the usefull messages
	GotMsg, Sender, Receiver = PRIVMSGHandler(IRCMsg)

	#Not Sent to me (probably sent to channel)
	global Nickname
	if Receiver != Nickname:
		print("Not PRIVMSG to me")
		return

	#Task b: Daily horoscope
	global 	Constellations
	if GotMsg.lower() in Constellations:
		print("\r\n----------Handle task b----------")
		TaskB(IRCSocket, Sender, GotMsg)
		print("----------End task b----------\r\n")
		return

	#Task c: Guess Number
	if GotMsg == "!guess":
		print("\r\n----------Handle task c----------")
		TaskC(IRCSocket, Sender)
		print("----------End task c----------\r\n")
		return

	#Task d: Music robot
	if GotMsg.split(" ", 1)[0] == "!song":
		print("\r\n----------Handle task d----------")
		TaskD(IRCSocket, Sender, GotMsg)
		print("----------End task d----------\r\n")
		return

	#Task e: Chat
	if GotMsg == "!chat":
		print("\r\n----------Handle task e----------")
		TaskE(IRCSocket, Sender)
		print("----------End task e----------\r\n")
		return

if __name__ == "__main__":
	#Task a: Connection to Channel & Automatic Introduction Message
	IRCSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	print("==========Socket Created==========")
	HostIP = input("Host IP:")
	PortNumber = int(input("Port:"))
	IRCSocket.connect((HostIP, PortNumber))
	print("==========Connected to server==========")

	#Send NICK Nickname
	Nickname = "bot_b05902030"
	SendMsg(IRCSocket, "NICK " + Nickname)

	#Send USER Username
	Username = "b05902030"
	SendMsg(IRCSocket, "USER " + Username)

	#Send JOIN #Channel
	Channel = "CN_DEMO"
	SendMsg(IRCSocket, "JOIN #" + Channel)
	print("==========Joined #" + Channel + "==========")

	#Automatic Introduction Message
	SendPRIVMSG(IRCSocket, "#" + Channel, "I'm " + Username)

	#Create Stdin Thread
	CreateStdinThread()

	#Create Socket and connect to stdin socket to get non-blocking stdin
	StdinSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ConnectStdin()

	#For select()
	ReadList = [IRCSocket, StdinSocket]
	global Connected
	Connected = True
	while Connected:
		rl, wl, error = select.select(ReadList, [], [])
		for fd in rl:
			if fd is IRCSocket:
				IRCMsg = IRCSocket.recv(4096).decode().strip("\r\n")
				print(IRCMsg)

				IRCMsgHandler(IRCSocket, IRCMsg)

			if fd is StdinSocket:
				StdinMsg = StdinSocket.recv(4096).decode().strip("\r\n")
				if StdinMsg == "QUIT":
					SendMsg(IRCSocket, StdinMsg)
					Connected = False
					break

	#Join the stdin thread, close all sockets, then exit
	global StdinThread
	StdinThread.join()
	IRCSocket.close()
	StdinSocket.close()

	exit()