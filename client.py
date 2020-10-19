#!/usr/bin/python
from socket import *
serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
response1 = clientSocket.recv(2048)
print(response1.decode())
print("1.CAPABILITY    2.LOGIN    3.NOOP    4.LOGOUT")
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

	clientSocket.sendall(command.encode())
	serverResponse = clientSocket.recv(2048)
	print(serverResponse.decode().strip())

	if(choice == 4):
		print("Connection closed by foreign host.")
		break
clientSocket.close()
