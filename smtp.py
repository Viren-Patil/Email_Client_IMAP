import smtplib
import imghdr
from email.message import EmailMessage
import csv

octetStreamFileTypes = ('.pdf', '.ppt', '.pptx', '.txt', '.py', '.odg', '.doc', '.docx', '.sh', '.c')

def send_the_mail(From, To, Subject, Message, Password, Attachments):
    msg = EmailMessage()
    msg['Subject'] = Subject
    msg['From'] = From
    
    if not To:
        f = open("recipients.csv",'r')
        Receipients = []
        for line in f:
            ln = line.split(',')
            ln[-1] = ln[-1].replace('\n', '')
            Receipients.append(ln[-1])

        msg['To'] = ', '.join(Receipients)

    else:
        msg['To'] = To

    msg.set_content(Message)

    for attachment in Attachments:
        # print(attachment)
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_name = f.name

            if file_name.lower().endswith(octetStreamFileTypes):
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            else:
                file_type = imghdr.what(f.name)
                msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(From, Password)
        smtp.send_message(msg)
        