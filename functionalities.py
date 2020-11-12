import os
import sys
import string
import random

def printMenu():
	print("1.CAPABILITY        2.LOGIN              3.LOGOUT    4.CREATE             5.DELETE MAILBOX       6.RENAME")
	print("7.SELECT MAILBOX    8.DESELECT MAILBOX   9.READING   10.DELETE MAIL(S)    11.LIST THE MAILBOXES  12.SEND MAIL (SMTP)")

def get_alphanumeric_string():
	opt = string.ascii_letters + string.digits
	alphanumeric_string = ''.join((random.choice(opt) for i in range(6)))
	return alphanumeric_string

def capability():
	command = "CAPABILITY\r\n"
	return command

def login(username, passwd):
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
	command = "FETCH " + str(mail_no) + ":" + str(mail_no) + " rfc822.header\r\n"
	return command
	
def read_size_mail(mail_no):
	command = "FETCH " + str(mail_no) + ":" + str(mail_no) + " rfc822.size\r\n"
	return command
	
def read_message(mail_no):
	command = "FETCH " + str(mail_no) + ":" + str(mail_no) + " rfc822.text\r\n"
	return command

def store(uid):
	command = "STORE " + str(uid) + ":" + str(uid) + " +FLAGS (\Deleted)\r\n"
	return command
	
def expunge():
	return "EXPUNGE\r\n"
	
def list_mailbox():
	command = 'LIST "" %\r\n'
	return command

def search_seen():
	command = "SEARCH SEEN\r\n"
	return command

def search_recent():
	command = "SEARCH RECENT\r\n"
	return command

def search_unseen():
	command = "SEARCH UNSEEN\r\n"
	return command

def search_unseen():
	command = "SEARCH UNSEEN\r\n"
	return command

def extracter_email(response):
	l = response.split("\n")
	length = len(l)
	Cc = None
	Subject = None
	for n in range(length):
		l[n] = l[n].strip().split(" ")
	for i in range(length):
		if l[i][0] == "To:":
			To = " ".join(l[i][1:])
		if l[i][0] == "Cc:":
			Cc = l[i][1:]
		if l[i][0] == "From:":
			From = " ".join(l[i][1:])
		if l[i][0] == "Date:":
			Date = ' '.join(l[i][1:])
		if l[i][0] == "Subject:":					
			Subject = ' '.join(l[i][1:])
	return (To, Cc, From, Date, Subject)
	
	
	
def executeCommand(clientSocket, command):
    alp_num_string = get_alphanumeric_string()
    command = alp_num_string + " " + command
    clientSocket.sendall(command.encode())
    serverResponse = clientSocket.recv(2048)
    return serverResponse.decode().strip()

def executeCommand_smtp(smtpSocket, command):
	smtpSocket.sendall(command.encode())
	serverResponse = smtpSocket.recv(2048)
	return serverResponse.decode().strip()

def clearScreen():
	os.system('clear')
	printMenu()

def printInputLine(param=None):
	if param:
		print(param + " (-1 to clear screen))> ", end='')
		choice = int(input())
	else:
		choice = int(input("\n(logged-out (-1 to clear screen))> "))

	return choice


