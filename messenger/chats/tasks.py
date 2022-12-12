from datetime import datetime

from django.core.mail import send_mail

from application.celery import app
from application.settings import ADMINS, EMAIL_HOST_USER
from users.models import User


@app.task()
def send_email_chat_created(chat_title):
    send_mail(
        subject='New chat was created',
        message=f'Why are you reading this? Haven`t you seen the subjects\n'
                f'Urgh, OKAY, chat name is {chat_title}',
        from_email=EMAIL_HOST_USER,
        recipient_list=ADMINS
    )


@app.task()
def count_system_users():
    users = User.objects.all()
    quantity = users.count()

    # date = datetime.now().strftime()

    with open('log-file.txt', 'a') as file:
        file.write(f'User count is: {quantity} --\n')
