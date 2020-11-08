#!/usr/bin/python
from socket import *
from functionalities import *

serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
resp = clientSocket.recv(2048).decode()
if 'OK' in resp:
	print("Connected to the IMAP Server ...\nFollowing are the functionalities of this Email Client ...\n")
	print("1.CAPABILITY        2.LOGIN              3.LOGOUT    4.CREATE             5.DELETE               6.RENAME")
	print("7.SELECT MAILBOX    8.DESELECT MAILBOX   9.READING   10.DELETE MAIL(S)    11.LIST THE MAILBOXES")
else:
	print("Sorry couldn't connect to the IMAP server!")
	sys.exit()

logged_in = []
selected_state = []
login_state_commands = [1,3,4,5,6,7,8,9,10,11]
selected_state_commands = [8,9,10]
logout_state_commands = [1,2,3]

while True:
	try:
		if len(logged_in) != 0:
			if logged_in[1]:
				print("\n(STATUS: logged in (" + logged_in[0] + "))> ", end='')
				choice = int(input())
		else:
			choice = int(input("\n(STATUS: logged out)> "))

		if choice == 1:
			command = capability()
			print(executeCommand(clientSocket, command))
			continue

		elif choice == 2:
			username = input("Username: ")
			passwd = input("Password: ")
			command = login(username, passwd)
			executed_command = executeCommand(clientSocket, command)

			if "OK" in executed_command:
				logged_in.append(username)
				logged_in.append(True)
				print("Login Successful!")

			elif "NO" in executed_command:
				print("Invalid User or Password!")

			elif "BAD" in executed_command:
				print("Try again!")

			continue

		elif choice == 3:
			command = logout()
			print(executeCommand(clientSocket, command))
			print("Connection closed by foreign host.")
			break

		elif choice == 4:
			mailbox = input("Name of mailbox to be created: ")
			command = create(mailbox)
			executed_command = executeCommand(clientSocket, command)

			if "OK" in executed_command:
				print("Created mailbox " + str(mailbox) + " successfully!")

			elif "BAD" in executed_command:
				print("Cannot create mailbox in logged out state.")
			
			elif "NO" in executed_command:
				print("A mailbox with that name already exists. Try another name")

			continue

		elif choice == 5:
			mailbox = input("Name of mailbox to be deleted: ")
			command = delete(mailbox)
			executed_command = executeCommand(clientSocket, command)

			if "OK" in executed_command:
				print("Mailbox " + mailbox + " deleted successfully!")
			
			elif "NO" in executed_command:
				print("Mailbox " + mailbox + " doesn't exist!")
			
			elif "BAD" in executed_command:
				print("Invalid mailbox name! Try again!")
			
			continue

		elif choice == 6:
			mailbox = input("Name of mailbox: ")
			new_name = input("New name: ")
			command = rename(mailbox, new_name)
			executed_command = executeCommand(clientSocket, command)

			if "OK" in executed_command:
				print("Successfully changed the name of mailbox from " + str(mailbox) + " to " + str(new_name))
			
			elif "NO" in executed_command:
				command = list_mailbox()
				executed_command = executeCommand(clientSocket, command)
				temp = executed_command.split("\n")
				ls = list()
				for i in temp:
					i = i.strip().split(" ")
					ls.append(i[-1])
				ls.pop()
				
				if mailbox not in ls:
					print("Mailbox " + str(mailbox) + " doesn't exist!")

				if new_name in ls:
					print("Mailbox can't be renamed with " + str(new_name) + " as " + str(new_name) + " already exists.")
			
			elif "BAD" in executed_command:
				print("Invalid arguments! Try again!")

			continue

		elif choice == 7:
			mailbox = input("Name of mailbox: ")
			command = select(mailbox)
			executed_command = executeCommand(clientSocket, command)

			if "OK" in executed_command:
				print("Mailbox " + mailbox + " has been selected")
				selected_state.append(mailbox)
				selected_state.append(True)
			
			elif "NO" in executed_command:
				print("Mailbox " + mailbox + " does not exist!")
			
			elif "BAD" in executed_command:
				print("Invalid mailbox name!")
			
			continue

		elif choice == 8:
			command = close()
			executed_command = executeCommand(clientSocket, command)

			if "OK" in executed_command:
				print("Closed mailbox " + selected_state[0] + " successfully!")
				while len(selected_state) != 0:
					selected_state.pop()

		elif choice == 9:
			uid = int(input("uid of mail: "))
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
			mail = From + '\n' + Subject + '\n' + To + '\n' + Date + '\n\n' + Message + '\n'	
			print(mail)
			continue

		elif choice == 10:
			uid = int(input("UID of mail to be deleted: "))
			command = store(uid)
			executeCommand(clientSocket, command)
			command = expunge()
			executed_command = executeCommand(clientSocket, command)
			if "OK" in executed_command:
				print("Deleted mail with UID: " + str(uid) + " successfully!")
			elif "NO" in executed_command:
				print("Can't delete that mail! Permission Denied!")
		
		elif choice == 11:
			command = list_mailbox()
			executed_command = executeCommand(clientSocket, command)
			temp = executed_command.split("\n")

			ls = list()
			for i in temp:
				i = i.strip().split(" ")
				ls.append(i[-1])
			ls.pop()

			if "OK" in executed_command:
				print("List of mailboxes: ", end=" ")
				for i in ls:
					print(i, end = " ")
			else:
				print("Couldn't list the mailboxes")

			continue
			

		# print(executeCommand(clientSocket, command))

	except:
		print("\nInvalid Input ...\nTry again!")

clientSocket.close()


# elif choice == 3:
# 	command = noop()

# if subchoice == 101:
# 	command = read_header_mail(uid)
# elif subchoice == 102:
# 	command = read_size_mail(uid)
# elif subchoice == 103:
# 	command = read_complete_mail(uid)

# elif choice == 11:
# 	command = check()

# elif choice == 9:
# 	mailbox = input("Name of mailbox: ")
# 	command = examine(mailbox)

# elif choice == 10:
# 	mailbox = input("Name of mailbox: ")
# 	subchoice = int(input("101.MESSAGES\t102.RECENT\t103.UIDNEXT\t104.UIDVALIDITY\t105.UNSEEN: "))
# 	if subchoice == 101:
# 	#no of messages in the mailbox
# 		command = "STATUS " + mailbox + " (MESSAGES)\r\n"
# 	elif subchoice == 102:
# 	#no of messages with recent flag set
# 		command = "STATUS " + mailbox + " (RECENT)\r\n"
# 	elif subchoice == 103:
# 	#next unique identifier of the mailbox
# 		command = "STATUS " + mailbox + " (UIDNEXT)\r\n"
# 	elif subchoice == 104:
# 	#unique identifier value of the mailbox
# 		command = "STATUS " + mailbox + " (UIDVALIDITY)\r\n"
# 	elif subchoice == 105:
# 	#no of messages which do not have seen flag set
# 		command = "STATUS " + mailbox + " (UNSEEN)\r\n"

# elif choice == 14:
# 	command = expunge()
