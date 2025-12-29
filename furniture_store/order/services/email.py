from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    """
    Sends order confirmation email to the user
    """
    user = order.user

    subject = f"Order Confirmation - Order #{order.id}"

    message = (
        f"Hello {user.email},\n\n"
        f"Your order has been placed successfully.\n\n"
        f"Order ID: {order.id}\n"
        f"Total Amount: {order.total_price}\n"
        f"Order Status: {order.status}\n\n"
        f"Delivery Address:\n"
        f"{order.full_address}\n\n"
        f"Thank you for shopping with us."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
