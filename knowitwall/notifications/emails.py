from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMessage
import threading
from config.settings import ADMIN_LIST

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, 'emailtoknowitwall@gmail.com', self.recipient_list)
        msg.content_subtype = "html"
        msg.send()

def send_email(message, subject='Knowitwall feedback!', recipient_list=ADMIN_LIST):
    EmailThread(subject=subject, html_content=message, recipient_list=recipient_list).run()
