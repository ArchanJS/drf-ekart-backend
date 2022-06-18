from django.conf import settings
from django.core.mail import send_mail

def verifyEmail(email,key):
    try:
        subject="Email verification"
        message="Your key is {}".format(key)
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email,]
        send_mail(subject,message,email_from,recipient_list)
    except Exception as e:
        print(e)
        return False
    return True