"""Модуль orders/services/notifications.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.template.loader import render_to_string
from core.utils.email import send_html_email
from orders.models import Order, PaymentMethod
from orders.services.invoice_pdf import generate_order_invoice_pdf

def send_order_email(order: Order) -> None:
    """Виконує логіку `send_order_email`.

Args:
    order: Вхідне значення для виконання операції.

Returns:
    None."""
    context = {'order': order, 'online_payment_links': {'Portmone': 'https://www.portmone.com.ua/', 'EasyPay': 'https://easypay.ua/ua', 'iPay': 'https://ipay.ua/', 'Masterpass': 'https://www.mastercard.ua/'}}
    html_body = render_to_string('avelon_healthcare/orders/emails/order_email.html', context)
    attachments = []
    if order.payment_method in {PaymentMethod.BANK_TRANSFER, PaymentMethod.ONLINE}:
        invoice_pdf = generate_order_invoice_pdf(order)
        attachments.append((f'invoice_order_{order.id}.pdf', invoice_pdf, 'application/pdf'))
    send_html_email(subject=f'Avelon Healthcare — замовлення #{order.id}', html_body=html_body, to=[order.email], attachments=attachments)
