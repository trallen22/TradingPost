import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email():

    addresses = ["michaelgkelly01@yahoo.com", "secharmot@davidson.edu", "lehu@davidson.edu"]

    for address in addresses:
        '''This is the email address I created and used. You will have to make your own and 
        google how to automate sending emails via gmail'''
        fromaddr = "etf.scraper@gmail.com"
        toaddr = address

        # instance of MIMEMultipart
        msg = MIMEMultipart()
        
        # storing the senders email address  
        msg['From'] = fromaddr
        
        # storing the receivers email address 
        msg['To'] = toaddr
        
        # storing the subject 
        msg['Subject'] = "Daily ETF Information"
        
        # string to store the body of the mail
        body = "Hello team, please see the attachment for the indicators."
        
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        
        # open the file to be sent 
        filename = "etf.csv"
        attachment = open("etf.csv", "rb")
        
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        
        # encode into base64
        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        
        # start TLS for security
        s.starttls()
        
        # Authentication
        ''' You will need to add your own authentication here after creating your own gmail account.'''
        s.login(fromaddr, "")
        
        # Converts the Multipart msg into a string
        text = msg.as_string()
        
        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
        
        # terminating the session
        s.quit()

send_email()