#!/usr/bin/python
from socket import *
from functionalities import *
import config as conf
from smtp import *
import getpass
from tabulate import tabulate

# This variable maintains count of emails present in mailbox
global mno

serverName = '127.0.0.1'
serverPort = 143
clientSocket = create_connection((serverName, serverPort))
resp = clientSocket.recv(2048).decode()

if 'OK' in resp:
	print("Connected to the IMAP Server ...\nFollowing are the functionalities of this Email Client ...\n")
	print("1.CAPABILITY          2.LOGIN              3.LOGOUT      4.CREATE             5.DELETE MAILBOX        6.RENAME")
	print("7.SELECT MAILBOX      8.CLOSE MAILBOX      9.READING     10.DELETE MAIL(S)    11.LIST THE MAILBOXES   12.SEND MAIL (SMTP)")
	print("13.SMTP ON LOCALHOST  14.QUIT")
else:	
	print("Sorry couldn't connect to the IMAP server!")
	sys.exit()

logged_in = [None, False] 
selected_state = [None, False] #selected state means mailbox is selected 

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
					
		if choice == -1:  #for clearing the screen
			clearScreen()

		elif choice == 1: #Capability
			command = capability()
			print(executeCommand(clientSocket, command))

		elif choice == 2: #Login
			if conf.provide_login_credentials_imap_explicitly:
				username = input("Username: ")
				passwd = getpass.getpass() #so that user can't see password while entering credentials
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
					print("Try again! (Cannot login in logged in state)")


		elif choice == 3: #Logout
			if logged_in[1] == False:
				print("You are already logged out!")
			else:
				command = logout()
				logged_in = [None, False]
				if conf.server_replies:
					print(executeCommand(clientSocket, command))
					print("Connection closed by foreign host.")
				else:
					print("Logging out! Bye! Connection closed")
				clientSocket.close()
				clientSocket = create_connection((serverName, serverPort))
				continue


		elif choice == 4: #Creating Mailbox
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


		elif choice == 5: #Deleting mailbox
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


		elif choice == 6: #Renaming mailbox
			mailbox = input("Name of mailbox: ")
			new_name = input("New name: ")
			command = rename(mailbox, new_name)
			executed_command = executeCommand(clientSocket, command)

			if conf.server_replies:
				print(executed_command)

			else:
				if "OK" in executed_command:
					print("Successfully changed the name of mailbox from " + str(mailbox) + " to " + str(new_name))
				
				elif "NO" in executed_command: #Logic for checking the reason behind not able to rename 
											   # the mailbox. 
					command = list_mailbox()
					executed_command = executeCommand(clientSocket, command)
					temp = executed_command.split("\n")        #temp is list of strings
					ls = list()
					for i in temp:
						i = i.strip().split(" ")				#converting list of strings to list of lists
						ls.append(i[-1])
					ls.pop()
					
					if mailbox not in ls:
						print("Mailbox " + str(mailbox) + " doesn't exist!")

					if new_name in ls:
						print("Mailbox can't be renamed with " + str(new_name) + " as " + str(new_name) + " already exists.")
				
				elif "BAD" in executed_command:
					print("Invalid arguments! Try again!")


		elif choice == 7: #Selecting mailbox
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


		elif choice == 8: #Deselecting mailbox
			if selected_state[1] == False:
				print("You have not selected any mailbox")
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


		elif choice == 9: #Fetching and reading of mails
			if selected_state[1] == False:
				print("You have not selected an inbox")
			else:
				command = "SELECT " + selected_state[0] + '\r\n'
				
				#parsing of count of emails present in the mailbox from response of SELECT command
				x = executeCommand(clientSocket, command)
				temp2 = x.split("\n")
				for a in range(len(temp2)):
					temp = temp2[a].strip().split(" ")
					if 'EXISTS' in temp:
						mno = int(temp[1])
						break
				
				#Asking user the no of mails he want to see in tabular form		
				user_required_no_mails = int(input(f"How many mails do you want to fetch? ({mno} mails in your {selected_state[0]})\n"))
				if user_required_no_mails > mno or user_required_no_mails < 1:
					print(f"you can fetch upto {mno} mails only!") 
					continue	
				
				#List of uids of recent mails (count = user specified above)	
				mails_to_be_displayed = [i for i in range(mno - user_required_no_mails + 1, mno + 1)]	
				
				#Creating list of uids of \SEEN mails
				seen_uids = executeCommand(clientSocket, search_seen())
				seen_uids = ((seen_uids.split('\n')[0]).strip().split(" "))[2:]
				seen_uids = [int(i) for i in seen_uids]
				
				#Creating list of uids of \UNSEEN mails
				unseen_uids = executeCommand(clientSocket, search_unseen())
				unseen_uids = ((unseen_uids.split('\n')[0]).strip().split(" "))[2:]
				unseen_uids = [int(i) for i in unseen_uids]
				
				mail_list = list()
				
				for u in mails_to_be_displayed:
					command = read_header_mail(u) #function to find only headers
					response = executeCommand(clientSocket, command)

					To, Cc, From, Date, Subject = extracter_email(response)	#extracter_mail function parses required data and returns as tuple
					if u in unseen_uids:	
						mail = ["* ", str(u),From, Subject, Date]
						
					else:
						mail = ["  ", str(u),From, Subject, Date]
						
					mail_list.append(mail)	
				print(tabulate(mail_list, headers=["Unseen", "uid", "From", "Subject", "Date"], tablefmt="psql", colalign=("center", "center", "center", "left", "center")))
				
				
				user_required_mail = int(input("Which message do you want to read? [-1 to stop reading]\n"))
				while user_required_mail != -1:
				
					if user_required_mail > mno or user_required_mail < 0:
						print(f"you can fetch upto {mno} mails only!")
						user_required_mail = int(input("Which message do you want to read? [-1 to stop reading]\n"))
					else:
						command1 = read_header_mail(user_required_mail)
						response1 = executeCommand(clientSocket, command1)
						To, Cc, From, Date, Subject = extracter_email(response1)	
					
						command2 = read_message(user_required_mail) #read_message only fetches message
						response2 = executeCommand(clientSocket, command2)
						print("\n")
						print("From: ", From)
						
						#Sometimes mail may not have subject, cc, etc. 
						#In that case, those variables will be None as per extracter_mail function
						#and hence that info will not print accordingly
	
						if Subject:
							print("Subject: ", Subject)
						print("To: ", To)
						if Cc:
							print("Cc: ", Cc)
						print("Date: ", Date) 
						l = response2.split("\n")
						
						#removing redundant lines
						if l[-3] == '\r' and l[-4] == '\r':
							l.pop(-3)
							l.pop(-3)
						length = len(l)
						
						#printing parsed message
						for b in range(1, length - 2):
							print(l[b])
						user_required_mail = int(input("\n\nWhich message do you want to read? [-1 to stop reading]\n"))
					

		elif choice == 10:
			if selected_state[1] == False:
				print("You have not selected an inbox")
			else:
				uid = input("UID of mail(s) (space separated values if multiple to be deleted): ")
				uid_list = [int(i) for i in uid.split()]
				
				#store command sets the delete flag of messages from uid_list
				for u in uid_list:
					command = store(u)  
					executeCommand(clientSocket, command)
				#expunge deletes all those mails whose delete flag is set
				command = expunge()
				executed_command = executeCommand(clientSocket, command)

				if conf.server_replies:
					print(executed_command)
				
				else:
					if "OK" in executed_command:
						print("Deleted mail with UID: " + str(uid) + " successfully!")
					elif "NO" in executed_command:
						print("Can't delete that mail! Permission Denied!")

		
		elif choice == 11: #list all the mailboxes available for that particular user
			command = list_mailbox()
			executed_command = executeCommand(clientSocket, command)

			if conf.server_replies:
				print(executed_command)
			
			else:
				#parsing of names of mailboxes
				temp = executed_command.split("\n")
				ls = list()
				for i in temp:
					i = i.strip().split(" ")
					ls.append(i[-1]) 
				ls.pop()	#removing some redundant value which is not the name of mailbox

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
		
		elif choice == 13:
			user = logged_in[0]+ "@localhost"
			receiver = input("Enter receiver(s): ").split() #must be space separated
			subject = input("Enter subject: ")
			Message = list()
			message = input("Enter Message(Enter '.' on a new line to end input):\n")
			Message.append(message)
			while message != ".":
				message = input()
				Message.append(message)
			Message.pop()        #removing "." which was also appended

			serverName = '127.0.0.1'			
			serverPort = 25 #Port for smtp

			#No need to close connection on port 143 before establishing
			#connection on port 25
			
			smtpSocket = create_connection((serverName, serverPort))
			resp = smtpSocket.recv(2048).decode()
			if conf.server_replies:
				print(resp)
				
			#passing data in cmd1,2,3 as per required syntax
			cmd1 = "MAIL FROM: " + user + "\r\n"
			resp1 = executeCommand_smtp(smtpSocket, cmd1)
			if conf.server_replies:
				print(resp1)
			for recipient in receiver:
				cmd2 = "RCPT TO: " + recipient + "\r\n"
				resp2 = executeCommand_smtp(smtpSocket, cmd2)
				if conf.server_replies:
					print(resp2)

			cmd3 = "DATA\r\n"
			resp3 = executeCommand_smtp(smtpSocket, cmd3)
			if conf.server_replies:
				print(resp3)

			cmd4 = "Subject: " + subject + "\n" + "\n".join(Message) + "\r\n.\r\n"
			#print(cmd4)
			resp4 = executeCommand_smtp(smtpSocket, cmd4)
			if conf.server_replies:
				print(resp4)
			if "queued" in resp4:
				print("Mail sent Successfully!")
			else:
				print("Cannot send mail, Enter valid recipients")

		elif choice == 14: #Quit
			print("Closing Email Client...\n")
			break

		else:
			print("INVALID CHOICE!")
	except Exception as err:
		print(err)
		print("\nInvalid Input ...\nTry again!")

clientSocket.close()

