import sys
import string
import random

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

def store(uid):
	command = "STORE " + str(uid) + ":" + str(uid) + " +FLAGS (\Deleted)\r\n"
	return command
	
def expunge():
	return "EXPUNGE\r\n"
	
def list_mailbox():
	command = 'LIST "" %\r\n'
	return command

def executeCommand(clientSocket, command):
    alp_num_string = get_alphanumeric_string()
    command = alp_num_string + " " + command
    clientSocket.sendall(command.encode())
    serverResponse = clientSocket.recv(2048)
    return serverResponse.decode().strip()

