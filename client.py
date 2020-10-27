#!/usr/bin/python
from socket import *
import string
import random

serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
response = clientSocket.recv(2048)
print(response.decode())
print("1.CAPABILITY   2.LOGIN   3.NOOP   4.LOGOUT   5.CREATE   6.DELETE   7.RENAME   8.SELECT   9.EXAMINE   10.STATUS   11.CHECK   12.CLOSE	13.READING	14.EXPUNGE")

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


def check():
	command = "CHECK\r\n"
	return command

def close():
	command = "CLOSE\r\n"
	return command

def read_complete_mail(uid):
	command = "FETCH " + str(uid) + ":" + str(uid) + " rfc822\r\n"
	return command

def read_header_mail(mail_no):
	command = "FETCH " + str(uid) + ":" + str(uid) + " rfc822.header\r\n"
	return command
	
def read_size_mail(mail_no):
	command = "FETCH " + str(uid) + ":" + str(uid) + " rfc822.size\r\n"
	return command
	
def expunge():
	return "EXPUNGE"
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
		subchoice = int(input("101.MESSAGES	102.RECENT	103.UIDNEXT	104.UIDVALIDITY		105.UNSEEN: "))
		if subchoice == 101:
		#no of messages in the mailbox
			command = "STATUS " + mailbox + " (MESSAGES)\r\n"
		elif subchoice == 102:
		#no of messages with recent flag set
			command = "STATUS " + mailbox + " (RECENT)\r\n"
		elif subchoice == 103:
		#next unique identifier of the mailbox
			command = "STATUS " + mailbox + " (UIDNEXT)\r\n"
		elif subchoice == 104:
		#unique identifier value of the mailbox
			command = "STATUS " + mailbox + " (UIDVALIDITY)\r\n"
		elif subchoice == 105:
		#no of messages which do not have seen flag set
			command = "STATUS " + mailbox + " (UNSEEN)\r\n"
			
	elif choice == 11:
		command = check()
	elif choice == 12:
		command = close()
	elif choice == 13:
		subchoice = int(input("101.HEADER	102.SIZE		103.COMPLETE MESSAGE"))
		uid = int(input("uid of mail: "))
		if subchoice == 101:
			command = read_header_mail(uid)
		elif subchoice == 102:
			command = read_size_mail(uid)
		elif subchoice == 103:
			command = read_complete_mail(uid)
	elif choice == 14:
		command = expunge()

	alp_num_string = get_alphanumeric_string()
	command = alp_num_string + " " + command
	clientSocket.sendall(command.encode())
	serverResponse = clientSocket.recv(2048)
	print(serverResponse.decode().strip())

	if(choice == 4):
		print("Connection closed by foreign host.")
		break
clientSocket.close()
