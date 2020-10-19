#!/usr/bin/python
from socket import *
serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
response1 = clientSocket.recv(2048)
print(response1.decode())
print("1.CAPABILITY    2.LOGIN    3.NOOP    4.LOGOUT	5.CREATE	6.DELETE	7.REMANE	8.SELECT	9.EXAMINE	10.STATUS	11.CHECK	12.CLOSE")
def capability():
	command = "a001 CAPABILITY\r\n"
	return command

def login():
	username = input("Username: ")
	passwd = input("Password: ")
	command = "a002 LOGIN " + username + " " + passwd + "\r\n" 
	return command

def noop():
	command = "a003 NOOP\r\n"
	return command

def logout():
	command = "a004 LOGOUT\r\n"
	return command
	
def create(mailbox):
	command = "a005 CREATE " + mailbox + '\r\n'
	return command

def delete(mailbox):
	command = "a006 DELETE " + mailbox + '\r\n'
	return command

def rename(mailbox, new_name):
	command = "a007 RENAME " + mailbox + " " + new_name + '\r\n'
	return command

def select(mailbox):
	command = "a008 SELECT " + mailbox + '\r\n'
	return command

def examine(mailbox):
	command = "a009 EXAMINE " + mailbox + '\r\n'
	return command

def status(mailbox, data_item_names):
	command = "a010 STATUS " + mailbox + " (" + data_item_names + ')\r\n'
	#STATUS name_of_mailbox UIDNEXT MESSAGES
	return command

def check():
	command = "a011 CHECK\r\n"
	return command

def close():
	command = "a012 CLOSE\r\n"
	return command


	

while True:
	choice = int(input())
	if choice == 1:
		command = capability()
	elif choice == 2:
		command = login()
	elif choice == 3:
		command = noop()
	elif choice == 4:
		command = logout()	
	elif choice == 5:
		mailbox = input("Name of mailbox: ")
		command = create(mailbox)
	elif choice == 6:
		mailbox = input("Name of mailbox to be deleted: ")
		command = delete(mailbox)
	elif choice == 7:
		mailbox = input("Name of mailbox: ")
		new_name = input("New name: ")
		command = rename(mailbox, new_name)
	elif choice == 8:
		mailbox = input("Name of mailbox: ")
		command = select(mailbox)
	elif choice == 9:
		mailbox = input("Name of mailbox: ")
		command = examine(mailbox)
	elif choice == 10:
		mailbox = input("Name of mailbox: ")
		data_item_names = input("Data item names: ")
		command = status(mailbox, data_item_names)
	elif choice == 11:
		command = check()
	elif choice == 12:
		command = close()

	clientSocket.sendall(command.encode())
	serverResponse = clientSocket.recv(2048)
	print(serverResponse.decode().strip())

	if(choice == 4):
		print("Connection closed by foreign host.")
		break
clientSocket.close()
