import requests
import os
import socket
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, date

import PRIVATE


class Email:
    sender = PRIVATE.email_sender
    password = PRIVATE.email_password
    receiver = PRIVATE.email_receiver
    host = PRIVATE.email_host
    smtp_port = 465


def wait_for_internet_connection():
    while True:
        try:
            socket.create_connection(('google.com', 80))
        except OSError:
            pass
        else:
            return


def send_mail(sender, password, receiver, host, context, mail, port):
    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, mail.as_string())


# waiting for internet connection.
wait_for_internet_connection()

# Get device Information.
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
public_ip_address = os.popen('curl -s ifconfig.me').readline()
device_information = requests.get(f"http://ip-api.com/json/{public_ip_address}").json()

# get the time and date
current_time = datetime.now().strftime('%H:%M:%S')
date = date.today().strftime('%d.%m.%Y')

# Building Email.
subject = f"Security warning for your device: {hostname}"
body = f'''If you just turned on your device "{hostname}", you can ignore this message.
Device-Name     = {hostname}
Local IP        = {ip_address}
Public IP       = {public_ip_address}
                  -{device_information['country']} ({device_information['countryCode']})
                  -{device_information['city']}
                  -{device_information['isp']}

Date            = {date}
Time            = {current_time} ({device_information['timezone']})
'''

# Building Email "header".
msg = EmailMessage()
msg['From'] = Email.sender
msg['To'] = Email.receiver
msg['Subject'] = subject
msg.set_content(body)

ssl_context = ssl.create_default_context()

# Sending Email and quid.
send_mail(Email.sender, Email.password, Email.receiver, Email.host, ssl_context, msg, Email.smtp_port)
quit()
