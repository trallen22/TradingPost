'''
Sends the email to the email list

log numbers 600-699
'''

import smtplib
from email.message import EmailMessage
import mimetypes
import os
import configuration_file as config 

# send_email: send an email to config.EMAILLIST via smtp with the Trading Post excel file attached 
# parameters: 
#       to - string, email address to send Trading Post to 
#       subject - string, what to put in the subject line 
#       message - string, message for body of the email  
# returns:  0 - successfully sent email 
#           1 - failed 
def send_email(to, subject, message):
    if config.EMAILADDRESS is None or config.EMAILPASSWORD is None:
        # no email address or password
        # something is not configured properly
        config.logmsg('ERROR', 600, 'email address or password is not set')
        return 1

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = config.EMAILADDRESS
    msg['To'] = to
    msg.set_content(message)

    mime_str, _ = mimetypes.guess_type(config.OUTPUTEXCEL) # full MIME type string -> type/subtype
    mime_type, mime_subtype = mime_str.split('/', 1)
    try:
        # try to add Trading Post as attachment to email 
        with open(config.OUTPUTEXCEL, 'rb') as ap:
            msg.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, \
                filename=os.path.basename(config.OUTPUTEXCEL))
        config.logmsg('DEBUG', 601, f'found file \'{config.OUTPUTEXCEL}\' to email')
    except Exception as e:
        config.logmsg('ERROR', 602, f'{e}')
        return 1
    try:
        # try to add TestPlatform as attachment to email 
        with open(config.OUTPUTEXCEL, 'rb') as ap:
            msg.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, \
                filename=os.path.basename(config.OUTPUTPLATFORM))
        config.logmsg('DEBUG', 608, f'found file \'{config.OUTPUTPLATFORM}\' to email')
    except Exception as e:
        config.logmsg('ERROR', 609, f'{e}')
        return 1

    try:
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # logging into smtp 
            try:
                smtp.login(config.EMAILADDRESS, config.EMAILPASSWORD)
                config.logmsg('DEBUG', 603, f'successfully logged into smtp')
            except Exception as e:
                config.logmsg('ERROR', 604, f'{e}')
                return 1
            # sending email via smtp 
            try:
                smtp.send_message(msg)
                config.logmsg('DEBUG', 605, f'successfully sent smtp message')
            except Exception as e:
                config.logmsg('ERROR', 606, f'{e}')
                return 1
    except Exception as e:
        config.logmsg('ERROR', 607, f'{e}')
        return 1

    return 0
