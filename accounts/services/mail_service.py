from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import importlib
from .mail_interface import MailService
from Backend import dependencies

logger = logging.getLogger("django")


username='ashzar638@gmail.com'
password='cstlshkgpoiwbhlj'


class ConcreteMailService(MailService):

    def send_mail(self, html, text, subject, from_email, to_emails):
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



        server=smtplib.SMTP(host='smtp.gmail.com',port=587)
        server.ehlo()
        server.starttls()

        server.login(username,password)
        server.sendmail(from_email,to_emails,msg_str)
        server.quit()

 
    def propareEmailBody(self, email):
    
        uniqueCode_service_instance = dependencies.uniqueCode_service_class
        
        token = uniqueCode_service_instance.getUniqueCode(self)
        to_emails = []
        to_emails.append(email)
        self.send_mail(html=token,text='Here is the code ',subject='verification',from_email='',to_emails=to_emails)
        logger.info('The verification code has been sent to the email')
        return token