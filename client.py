#!/usr/bin/python
from socket import *
from functionalities import *

serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
response = clientSocket.recv(2048)
print(response.decode())
print("1.CAPABILITY\t2.LOGIN\t3.NOOP\t4.LOGOUT\t5.CREATE\t6.DELETE\t7.RENAME\t8.SELECT")
print("9.EXAMINE\t10.STATUS\t11.CHECK\t12.CLOSE\t13.READING\t14.EXPUNGE\t15.DELETE MAIL(S)\t16.STORE")

while True:

	choice = int(input())

	if choice == 1:
		command = capability()

	elif choice == 2:
		command = login()
		response = executeCommand(clientSocket, command)
		temp = response.split(" ")
		if temp[1] == "OK":
			print("Login Successful!")
		elif temp[1] == "NO":
			print("Invalid User or Password!")
		else:
			print("Try again!")
		continue
	'''
	elif choice == 3:
		command = noop()
	'''
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
		subchoice = int(input("101.MESSAGES\t102.RECENT\t103.UIDNEXT\t104.UIDVALIDITY\t105.UNSEEN: "))
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
		uid = int(input("uid of mail: "))
		'''
		if subchoice == 101:
			command = read_header_mail(uid)
		elif subchoice == 102:
			command = read_size_mail(uid)
		elif subchoice == 103:
			command = read_complete_mail(uid)
		'''
		command = read_complete_mail(uid)
		x = executeCommand(clientSocket, command)
		l = x.split("\n")
		length = len(l)
		if str(l[7])[:2] == "To":
			To = str(l[7])
		if str(l[8])[:3] == "Cc":
			From = str(l[9])
			Subject = str(l[10])
			Cc = str(l[8])
			Date = str(l[12])
			Message = (l[20:length - 3])
		else:
			From = str(l[8])
			Subject = str(l[9])
			Date = str(l[11])
			Message = l[19: length - 3]
			message = ""
		for i in Message:
			message += i
		temp = message.split('\r')
		t = len(temp)
		Message = ""
		for m in range(t - 1):
			Message += temp[m] + '\n'
		command = From + '\n' + Subject + '\n' + To + '\n' + Date + '\n' + Message + '\n'	
		print(command)
		continue
	elif choice == 14:
		command = expunge()

	elif choice == 15:
		uid = int(input("uid of mail to be deleted: "))
		command = store(uid)

	print(executeCommand(clientSocket, command))

	if(choice == 15):
		command = expunge()
		print(executeCommand(clientSocket, command))

	if(choice == 4):
		print("Connection closed by foreign host.")
		break
clientSocket.close()
