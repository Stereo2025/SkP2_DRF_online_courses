import os
import stripe
import smtplib

from django.core.mail import send_mail
from dotenv import load_dotenv
from rest_framework.exceptions import ValidationError
from stripe.error import StripeError

from config.settings import EMAIL_HOST_USER

# Загрузка переменных окружения
load_dotenv()

# Установка ключа API
stripe.api_key = os.getenv('STRIPE_API_KEY')


def create_payment(obj, user):
    try:
        product = stripe.Product.create(name=obj.name)

        price = stripe.Price.create(
            unit_amount=int(obj.amount) * 100,
            currency='rub',
            product=product['id']
        )

        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {"price": price.id, "quantity": 1}
            ],
            mode="payment",
            client_reference_id=str(user.id)
        )
        return session
    except StripeError as e:
        print(f"An error occurred: {e.user_message}")
        return None


def check_payment(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid' or session.payment_status == 'complete':
            return session
        else:
            print(f"Payment status for session {session_id} is {session.payment_status}")
            return None

    except StripeError as e:
        print(f"An error occurred: {e.user_message}")
        return None


def send_mailing(client_list, subject, body):
    try:
        response = send_mail(
            subject,
            body,
            EMAIL_HOST_USER,
            client_list
        )
        return response
    except smtplib.SMTPException:
        raise smtplib.SMTPException
