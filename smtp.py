# Python code to illustrate Sending mail from
# your Gmail account
import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.office365.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("rutvikgm18.comp@coep.ac.in", "Pass@888")

# message to be sent
message = "Message_you_need_to_send"

# sending the mail
s.send_message([message], ["rutvikgm18.comp@coep.ac.in"],['rutvikmoharil2000@gmail.com'])

# terminating the session
s.quit()
