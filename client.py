#!/usr/bin/python
from socket import *
from functionalities import *
import config as conf
from smtp import *
import getpass
from tabulate import tabulate
global mno #This variable maintains count of emails present in mailbox

serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
resp = clientSocket.recv(2048).decode()

if 'OK' in resp:
	print("Connected to the IMAP Server ...\nFollowing are the functionalities of this Email Client ...\n")
	print("1.CAPABILITY        2.LOGIN              3.LOGOUT      4.CREATE             5.DELETE MAILBOX       6.RENAME")
	print("7.SELECT MAILBOX    8.CLOSE MAILBOX      9.READING     10.DELETE MAIL(S)    11.LIST THE MAILBOXES  12.SEND MAIL (SMTP)")
else:	
	print("Sorry couldn't connect to the IMAP server!")
	sys.exit()

logged_in = [None, False]
selected_state = [None, False]
login_state_commands = [1,3,4,5,6,7,8,9,10,11]
selected_state_commands = [8,9,10]
logout_state_commands = [1,2,3]

while True:
	try:
		if logged_in[1] and selected_state[1]:
			param = "\n(" + logged_in[0] + "[" + selected_state[0] + "]"
			choice = printInputLine(param)
			
		elif logged_in[1] and not selected_state[1]:
			param = "\n(" + logged_in[0]
			choice = printInputLine(param)

		else:
			choice = printInputLine()
					
		if choice == -1:
			clearScreen()

		elif choice == 1:
			command = capability()
			print(executeCommand(clientSocket, command))

		elif choice == 2:
			if conf.provide_login_credentials_imap_explicitly:
				username = input("Username: ")
				passwd = getpass.getpass()
			else:
				username = conf.login_credentials_for_imap["username"]
				passwd = conf.login_credentials_for_imap["password"]

			command = login(username, passwd)
			executed_command = executeCommand(clientSocket, command)
			
			if conf.server_replies:
				print(executed_command)
				logged_in[0] = username
				logged_in[1] = True
			
			else:
				if "OK" in executed_command:
					logged_in[0] = username
					logged_in[1] = True
					print("Login Successful!")

				elif "NO" in executed_command:
					print("Invalid User or Password!")

				elif "BAD" in executed_command:
					print("Try again!")


		elif choice == 3:
			command = logout()
			if conf.server_replies:
				print(executeCommand(clientSocket, command))
				print("Connection closed by foreign host.")
			else:
				print("Logging out! Bye! Connection closed")
			break


		elif choice == 4:
			mailbox = input("Name of mailbox to be created: ")
			command = create(mailbox)
			executed_command = executeCommand(clientSocket, command)

			if conf.server_replies:
				print(executed_command)

			else:
				if "OK" in executed_command:
					print("Created mailbox " + str(mailbox) + " successfully!")

				elif "BAD" in executed_command:
					print("Cannot create mailbox in logged out state.")
				
				elif "NO" in executed_command:
					print("A mailbox with that name already exists. Try another name")


		elif choice == 5:
			mailbox = input("Name of mailbox to be deleted: ")
			command = delete(mailbox)
			executed_command = executeCommand(clientSocket, command)

			if conf.server_replies:
				print(executed_command)
			
			else:
				if "OK" in executed_command:
					print("Mailbox " + mailbox + " deleted successfully!")
				
				elif "NO" in executed_command:
					print("Mailbox " + mailbox + " doesn't exist!")
				
				elif "BAD" in executed_command:
					print("Invalid mailbox name! Try again!")


		elif choice == 6:
			mailbox = input("Name of mailbox: ")
			new_name = input("New name: ")
			command = rename(mailbox, new_name)
			executed_command = executeCommand(clientSocket, command)

			if conf.server_replies:
				print(executed_command)

			else:
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


		elif choice == 7:
			mailbox = input("Name of mailbox: ")
			command = select(mailbox)
			executed_command = executeCommand(clientSocket, command)
			
			if conf.server_replies:
				print(executed_command)
				if "OK" in executed_command:
					selected_state[0] = mailbox
					selected_state[1] = True
			
			else:
				if "OK" in executed_command:
					print("Mailbox " + mailbox + " has been selected")
					selected_state[0] = mailbox
					selected_state[1] = True
				
				elif "NO" in executed_command:
					print("Mailbox " + mailbox + " does not exist!")
				
				elif "BAD" in executed_command:
					print("Invalid mailbox name!")


		elif choice == 8:
			if selected_state[1] == False:
				print("You have not selected an inbox")
			else:
				command = close()
				executed_command = executeCommand(clientSocket, command)

				if conf.server_replies:
					print(executed_command)
					if "OK" in executed_command:
						selected_state[0] = None
						selected_state[1] = False

				else:
					if "OK" in executed_command:
						print("Closed " + selected_state[0] + " successfully!")
						selected_state[0] = None
						selected_state[1] = False


		elif choice == 9:
			if selected_state[1] == False:
				print("You have not selected an inbox")
			else:
				command = "SELECT " + selected_state[0] + '\r\n'
				
				#parsing of count of emails present in the mailbox
				x = executeCommand(clientSocket, command)
				temp2 = x.split("\n")
				for a in range(len(temp2)):
					temp = temp2[a].strip().split(" ")
					if 'EXISTS' in temp:
						mno = int(temp[1])
						break
				user_required_no_mails = int(input(f"How many mails do you want to fetch?{[mno]}\n"))
				if user_required_no_mails > mno or user_required_no_mails < 1:
					print(f"you can fetch upto {mno} mails only!") 
					continue	
				mails_to_be_displayed = [i for i in range(mno - user_required_no_mails + 1, mno + 1)]	
				
				seen_uids = executeCommand(clientSocket, search_seen())
				seen_uids = ((seen_uids.split('\n')[0]).strip().split(" "))[2:]
				seen_uids = [int(i) for i in seen_uids]
				#print(seen_uids)
				unseen_uids = executeCommand(clientSocket, search_unseen())
				unseen_uids = ((unseen_uids.split('\n')[0]).strip().split(" "))[2:]
				unseen_uids = [int(i) for i in unseen_uids]
				#print(unseen_uids)
				mail_list = list()
				for u in mails_to_be_displayed:
					command = read_header_mail(u)
					response = executeCommand(clientSocket, command)

					To, Cc, From, Date, Subject = extracter_email(response)	
					if u in unseen_uids:	
						mail = ["* ", str(u),From, Subject, Date]
						#print(mail)
					else:
						mail = ["  ", str(u),From, Subject, Date]
						#print(mail)
					mail_list.append(mail)	
				print(tabulate(mail_list, headers=["Unseen", "uid", "From", "Subject", "Date"], tablefmt="psql", colalign=("center", "center", "center", "left", "center")))
				
				user_required_mail = int(input("Which message do you want to read?\n"))
				while user_required_mail != -1:
				
					if user_required_mail > mno or user_required_mail < 0:
						print(f"you can fetch upto {mno} mails only!")
						user_required_mail = int(input("Which message do you want to read?\n"))
					else:
						command1 = read_header_mail(user_required_mail)
						response1 = executeCommand(clientSocket, command1)
						To, Cc, From, Date, Subject = extracter_email(response1)	
					
						command2 = read_message(user_required_mail)
						response2 = executeCommand(clientSocket, command2)
						print("\n")
						print("From: ", From)
						if Subject:
							print("Subject: ", Subject)
						print("To: ", To)
						if Cc:
							print("Cc: ", Cc)
						print("Date: ", Date) 
						l = response2.split("\n")
						length = len(l)
						for b in range(1, length - 2):
							print(l[b])
						user_required_mail = int(input("Which message do you want to read?\n"))
					

		elif choice == 10:
			if selected_state[1] == False:
				print("You have not selected an inbox")
			else:
				uid = int(input("UID of mail to be deleted: "))
				command = store(uid)
				executeCommand(clientSocket, command)
				command = expunge()
				executed_command = executeCommand(clientSocket, command)

				if conf.server_replies:
					print(executed_command)
				
				else:
					if "OK" in executed_command:
						print("Deleted mail with UID: " + str(uid) + " successfully!")
					elif "NO" in executed_command:
						print("Can't delete that mail! Permission Denied!")

		
		elif choice == 11:
			command = list_mailbox()
			executed_command = executeCommand(clientSocket, command)

			if conf.server_replies:
				print(executed_command)
			
			else:
				temp = executed_command.split("\n")
				ls = list()
				for i in temp:
					i = i.strip().split(" ")
					ls.append(i[-1])
				ls.pop()

				if "OK" in executed_command:
					print("List of mailboxes:")
					for i in ls:
						print('    --> ', i)

				else:
					print("Couldn't list the mailboxes")


		elif choice == 12:
			if conf.provide_login_cerdentials_smtp_explicitly:
				From = input("From: ")
				Password = getpass.getpass()
			else:
				From = conf.login_credentials_for_smtp["email-id"]
				Password = conf.login_credentials_for_smtp["password"]

			To = None
			if not conf.multi_recipients:
				To = input("To: ")

			Subject = input("Subject: ")
			msg = ""
			Message = ""
			print("Enter Message(Enter '.' on a new line to end input):")
			while True:
				msg = input()
				if msg == '.':
					break
				Message += msg + '\n'
			send_the_mail(From, To, Subject, Message, Password, conf.attachments_for_mail)
			print("Sent mail!")

		else:
			print("INVALID CHOICE!")

	except Exception as err:
		print(err)
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
