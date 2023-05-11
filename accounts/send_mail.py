import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



username='ashzar638@gmail.com'
password='cstlshkgpoiwbhlj'

def send_mail(html=None,text='Email_body',subject='Hello word',from_email='',to_emails=[]):
    print("here in send_email1")
    assert isinstance(to_emails,list)
    msg=MIMEMultipart('alternative')
    msg['From']=username
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject
    txt_part=MIMEText(text,'plain')
    msg.attach(txt_part)


    html_part = MIMEText(f"<p>Here is your password reset token</p><h1>{html}</h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()

    print(msg_str)
    print("here in send_email2")

    server=smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    print("here in send_email3")
    server.login(username,password)
    print("here in send_email4")
    server.sendmail(from_email,to_emails,msg_str)
    print("here in send_email5")
    server.quit()