import smtplib
from email.message import EmailMessage

def send_the_mail(From, To, Subject, Message, Password):
    msg = EmailMessage()
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = To
    msg.set_content(Message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(From, Password)
        smtp.send_message(msg)