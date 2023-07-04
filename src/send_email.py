import smtplib
from email.message import EmailMessage
import configurationFile as config 

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

send_email(config.EMAILLIST[0], 'test email', 'this is a test')