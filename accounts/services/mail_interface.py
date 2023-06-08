from abc import ABC, abstractmethod


class MailService(ABC):
    @abstractmethod
    def send_mail(self, html, text, subject, from_email, to_emails):
        pass

    @abstractmethod
    def sendEmail(self, email):
        pass

