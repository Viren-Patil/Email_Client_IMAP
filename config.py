#!/usr/bin/bash
import sys

# False recommended
# Make True if you want to see the exact server replies.
server_replies = False

# Dictionary of credentials of the user on the system
login_credentials_for_imap = {
    "username": "",
    "password": ""
}

# Make False if you provide credentials in the 
# dictionary login_credentials_for_imap on line number 9 of this config file
provide_login_credentials_imap_explicitly = True

# Dictionary of credentials of the gmail account of any user who wants to send mail.
login_credentials_for_smtp = {
    "email-id": "",
    "password": ""
}

# Make False if you provide credentials in the 
# dictionary login_credentials_for_smtp on line number 19 of this config file
provide_login_cerdentials_smtp_explicitly = True

# Note: You can give multiple attachments in this list
attachments_for_mail = []

# Keep False when you want to send mail to only one person
# else keep True and fill the recipients.csv file provided to you with
# multiple recipients information
multi_recipients = False