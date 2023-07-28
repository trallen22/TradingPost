import smtplib
from email.message import EmailMessage
import mimetypes
import os
import configuration_file as config 

def send_email(to, subject, message):
    if config.EMAILADDRESS is None or config.EMAILPASSWORD is None:
        # no email address or password
        # something is not configured properly
        print('ERROR: email address or password is not set')
        return False

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = config.EMAILADDRESS
    msg['To'] = to
    msg.set_content(message)

    mime_str, _ = mimetypes.guess_type(config.OUTPUTEXCEL) # full MIME type string -> type/subtype
    mime_type, mime_subtype = mime_str.split('/', 1)
    with open(config.OUTPUTEXCEL, 'rb') as ap:
        msg.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype,
        filename=os.path.basename(config.OUTPUTEXCEL))

    try:
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            try:
                smtp.login(config.EMAILADDRESS, config.EMAILPASSWORD)
            except Exception as e:
                print(f'ERROR: Failed to login to email')
                print(f'{e}')
            try:
                smtp.send_message(msg)
            except Exception as e:
                print(f'ERROR: Failed to send email')
        return True
    except Exception as e:
        print(f'ERROR: Failed to send email')
        print(f'ERROR: {e}')

    return False
