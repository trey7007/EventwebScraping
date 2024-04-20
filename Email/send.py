
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


contacts = ['treyvincent@hotmail.com']

with open('./Email/emailcontents.html','r') as msgfile:
    msgtxt = msgfile.read()

msg = EmailMessage()
msg['Subject'] = 'Upcoming events, Madison!'
msg['From'] = EMAIL_ADDRESS
msg.set_content(msgtxt, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    for c in contacts:
        msg['To'] = c
        smtp.send_message(msg)