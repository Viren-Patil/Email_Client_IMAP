import os
import sys
import string
import random

# Printing the Menu on the screen.
def printMenu():
	print("1.CAPABILITY          2.LOGIN              3.LOGOUT    4.CREATE             5.DELETE MAILBOX        6.RENAME")
	print("7.SELECT MAILBOX      8.DESELECT MAILBOX   9.READING   10.DELETE MAIL(S)    11.LIST THE MAILBOXES   12.SEND MAIL (SMTP)")
	print("13.SMTP ON LOCALHOST  14.QUIT")

# Generates an alphanumeric string which is necessary to be passed with every command
# that is sent by the client to the IMAP server.
def get_alphanumeric_string():

	# Generates a token of length 6
	opt = string.ascii_letters + string.digits
	alphanumeric_string = ''.join((random.choice(opt) for i in range(6)))
	return alphanumeric_string

# CAPABILITY Command
def capability():
	command = "CAPABILITY\r\n"
	return command

# Login function to login different users on the system.
def login(username, passwd):
	command = "LOGIN " + username + " " + passwd + "\r\n" 
	return command

# Logout user function
def logout():
	command = "LOGOUT\r\n"
	return command

# Creates a mailbox
def create(mailbox):
	command = "CREATE " + mailbox + '\r\n'
	return command

# Deletes a mailbox
def delete(mailbox):
	command = "DELETE " + mailbox + '\r\n'
	return command

# Renames a mailbox
def rename(mailbox, new_name):
	command = "RENAME " + mailbox + " " + new_name + '\r\n'
	return command

# Selects a mailbox
def select(mailbox):
	command = "SELECT " + mailbox + '\r\n'
	return command

# Closes a mailbox
def close():
	command = "CLOSE\r\n"
	return command

# Fetches complete mails i.e. Headers + Message
def read_complete_mail(uid):
	command = "FETCH " + str(uid) + ":" + str(uid) + " rfc822\r\n"
	return command

# Fetches only the Headers of the mail
def read_header_mail(mail_no):
	command = "FETCH " + str(mail_no) + ":" + str(mail_no) + " rfc822.header\r\n"
	return command

# Fetches the size of the mail in bytes
def read_size_mail(mail_no):
	command = "FETCH " + str(mail_no) + ":" + str(mail_no) + " rfc822.size\r\n"
	return command

# Fetches only Message of the mail	
def read_message(mail_no):
	command = "FETCH " + str(mail_no) + ":" + str(mail_no) + " rfc822.text\r\n"
	return command

# Stores the \Deleted flag with a particular mail uid that is provided by the user.
def store(uid):
	command = "STORE " + str(uid) + ":" + str(uid) + " +FLAGS (\Deleted)\r\n"
	return command

# Permanently deletes all the mails with the \Deleted flags set	
def expunge():
	return "EXPUNGE\r\n"

# Lists all the mailboxes of the user
def list_mailbox():
	command = 'LIST "" %\r\n'
	return command

# Searches the mails which have \Seen flag set
def search_seen():
	command = "SEARCH SEEN\r\n"
	return command

# Searches the mails which have \Recent flag set
def search_recent():
	command = "SEARCH RECENT\r\n"
	return command

# Searches the mails which have \Unseen flag set
def search_unseen():
	command = "SEARCH UNSEEN\r\n"
	return command

# Parses and returns only the Headers of a mail
def extracter_email(response):
	l = response.split("\n")
	length = len(l)
	Cc = None
	Subject = None
	To = None
	Date = None
	for n in range(length):
		l[n] = l[n].strip().split(" ")      # converting list of strings to list of lists
		
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
	
# Executes a command related to the locahost IMAP server. Used almost in every choice in client.py	
def executeCommand(clientSocket, command):
    alp_num_string = get_alphanumeric_string()
    command = alp_num_string + " " + command
    clientSocket.sendall(command.encode())
    serverResponse = clientSocket.recv(2048)
    return serverResponse.decode().strip()

# Executes command related to the localhost SMTP server
def executeCommand_smtp(smtpSocket, command):  #alphanumeric token not required in smtp protocol
	smtpSocket.sendall(command.encode())
	serverResponse = smtpSocket.recv(2048)
	return serverResponse.decode().strip()

# Clears the screen
def clearScreen():
	os.system('clear')
	printMenu()

# Prints the prompt line on the terminal
def printInputLine(param=None):
	if param:
		print(param + " (-1 to clear screen))> ", end='')
		choice = int(input())
	else:
		choice = int(input("\n(logged-out (-1 to clear screen))> "))

	return choice

# Following commands are not used
def noop():
	command = "NOOP\r\n"
	return command

def examine(mailbox):
	command = "EXAMINE " + mailbox + '\r\n'
	return command

def check():
	command = "CHECK\r\n"
	return command