# Python code to illustrate Sending mail from
# your Gmail account
import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.office365.com', 587)

# start TLS for security
s.starttls()

# Authentication
username = input()
passwd = input()
s.login(username, passwd)

# message to be sent
message = "Message_you_need_to_send"

# sending the mail
s.send_message(username, , message)

# terminating the session
s.quit()
