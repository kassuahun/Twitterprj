# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.

msg = EmailMessage()
msg.set_content("cssaf sadfsdf as dsdf asd asdf af gas asdg adg a")

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'The contents of xyz'
msg['From'] = 'kassuahun@gmail.com'
msg['To'] = 'kassuahun@gmail.com'

# Send the message via our own SMTP server.
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
sender_address = 'nordicadvocacyteam@gmail.com'
sender_pass 
session.login(sender_address, sender_pass)

session.send_message(msg)
session.quit()