#!/usr/bin/bash
import sys

# False recommended
# Make True if you want a deeper understanding of what happens behind the scene.
server_replies = False

login_credentials_for_imap = {
    "username": "batman",
    "password": "batman"
}

# Make False if you provide credentials in the dict login_credentials_for_imap above
provide_login_credentials_imap_explicitly = False

login_credentials_for_smtp = {
    "email-id": "cnproject.emailclient@gmail.com",
    "password": "cnproject"
}

# Make False if you provide credentials in the dict login_credentials_for_smtp above
provide_login_cerdentials_smtp_explicitly = False

# Note: You can give multiple attachments in this list
attachments_for_mail = ['functionalities.py']