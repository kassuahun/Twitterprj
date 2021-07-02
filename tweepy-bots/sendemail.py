import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def sendEmail(receiver_address, subject,mail_content):
    
    #The mail addresses and password
    sender_address = 'nordicadvocacyteam@gmail.com'
    sender_pass = "ENN+46se+47no"
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject  #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return 'Mail Sent ' + to + " " + str(datetime.datetime.now().strftime("%c"))

# to = 'kassuahun@gmail.com'
# subject= "test as a function"

# mail_content = '''Hello, this is test with func.
#     This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
#     Thank You
#     '''
# print(sendEmail(to, subject, mail_content))