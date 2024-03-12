from django.core.mail import EmailMessage
from django.core.mail import send_mail
from smtplib import SMTPException


class Utils:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
            email.send()
        except SMTPException as e:
            # Handle the exception here
            print(f"An error occurred while sending the email: {e}")

        # send_mail(data['email_subject'], data['email_body'], 'sainshy.test@gmail.com', [data['to_email']])
