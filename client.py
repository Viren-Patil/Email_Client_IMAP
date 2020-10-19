#!/usr/bin/python
from socket import *
import string
import random

serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
response = clientSocket.recv(2048)
print(response.decode())
print("1.CAPABILITY   2.LOGIN   3.NOOP   4.LOGOUT   5.CREATE   6.DELETE   7.RENAME   8.SELECT   9.EXAMINE   10.STATUS   11.CHECK   12.CLOSE")

def get_alphanumeric_string():
	opt = string.ascii_letters + string.digits
	alphanumeric_string = ''.join((random.choice(opt) for i in range(6)))
	return alphanumeric_string

def capability():
	command = "CAPABILITY\r\n"
	return command

def login():
	username = input("Username: ")
	passwd = input("Password: ")
	command = "LOGIN " + username + " " + passwd + "\r\n" 
	return command

def noop():
	command = "NOOP\r\n"
	return command

def logout():
	command = "LOGOUT\r\n"
	return command
	
def create(mailbox):
	command = "CREATE " + mailbox + '\r\n'
	return command

def delete(mailbox):
	command = "DELETE " + mailbox + '\r\n'
	return command

def rename(mailbox, new_name):
	command = "RENAME " + mailbox + " " + new_name + '\r\n'
	return command

def select(mailbox):
	command = "SELECT " + mailbox + '\r\n'
	return command

def examine(mailbox):
	command = "EXAMINE " + mailbox + '\r\n'
	return command

def status(mailbox, data_item_names):
	command = "a010 STATUS " + mailbox + " (" + data_item_names + ')\r\n'
	#STATUS name_of_mailbox UIDNEXT MESSAGES
	return command

def check():
	command = "CHECK\r\n"
	return command

def close():
	command = "CLOSE\r\n"
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

	alp_num_string = get_alphanumeric_string()
	command = alp_num_string + " " + command
	clientSocket.sendall(command.encode())
	serverResponse = clientSocket.recv(2048)
	print(serverResponse.decode().strip())

	if(choice == 4):
		print("Connection closed by foreign host.")
		break
clientSocket.close()
