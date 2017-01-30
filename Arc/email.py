import smtplib
from email.mime.text import MIMEText


def send_text(address, subject, content):
    user = 'ParallelArcOfficial@outlook.com'
    pwd = '#superissubin#'
    host = 'smtp-mail.outlook.com'
    port = 587
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, address, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False
