#!/usr/bin/bash
import sys

# False recommended
# Make True if you want a deeper understanding of what happens behind the scene.
server_replies = False

login_credentials_for_imap = {
    "username": "",
    "password": ""
}

# Make False if you provide credentials in the dict login_credentials_for_imap above
provide_login_credentials_imap_explicitly = False

login_credentials_for_smtp = {
    "email-id": "",
    "password": ""
}

# Make False if you provide credentials in the dict login_credentials_for_smtp above
provide_login_cerdentials_smtp_explicitly = True

# Note: You can give multiple attachments in this list
attachments_for_mail = []

# Keep False when you want to send mail to only one person
# else keep True and fill the recipients.csv file provided to you.
multi_recipients = True

# receipients = ['viren.p2000@gmail.com', 'rutvikmoharil2000@gmail.com']
