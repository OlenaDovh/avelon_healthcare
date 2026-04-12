from __future__ import annotations

from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import AuthenticatedOrderForm, GuestOrderForm
from .models import Order, OrderStatus, PaymentMethod
from core.utils.email import send_html_email


def get_order_form(request: HttpRequest) -> GuestOrderForm | AuthenticatedOrderForm:
    """
    Повертає форму оформлення замовлення.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        GuestOrderForm | AuthenticatedOrderForm: Форма замовлення.
    """
    if request.user.is_authenticated:
        return AuthenticatedOrderForm(request.POST or None)

    return GuestOrderForm(request.POST or None)


def get_bank_transfer_auto_pay_after_minutes() -> int:
    """
    Повертає кількість хвилин для автопідтвердження оплати на рахунок.

    Returns:
        int: Кількість хвилин очікування.
    """
    value: int = int(getattr(settings, "BANK_TRANSFER_AUTO_PAY_AFTER_MINUTES", 5))
    return max(value, 1)


def update_bank_transfer_order_status(order: Order) -> None:
    """
    Автоматично змінює статус замовлення на сплачено для оплати на рахунок.

    Args:
        order (Order): Замовлення.

    Returns:
        None
    """
    if order.status != OrderStatus.NEW:
        return

    if order.payment_method != PaymentMethod.BANK_TRANSFER:
        return

    auto_pay_after_minutes: int = get_bank_transfer_auto_pay_after_minutes()
    paid_at_threshold = order.created_at + timezone.timedelta(minutes=auto_pay_after_minutes)

    if timezone.now() >= paid_at_threshold:
        order.status = OrderStatus.PAID
        order.paid_at = timezone.now()
        order.save(update_fields=["status", "paid_at"])


def update_bank_transfer_orders_status(orders: QuerySet[Order]) -> None:
    """
    Оновлює статуси замовлень з оплатою на рахунок.

    Args:
        orders (QuerySet[Order]): Набір замовлень.

    Returns:
        None
    """
    for order in orders:
        update_bank_transfer_order_status(order)


def generate_order_invoice_pdf(order: Order) -> bytes:
    """
    Генерує PDF-рахунок для замовлення.

    Args:
        order (Order): Замовлення.

    Returns:
        bytes: PDF у вигляді байтів.
    """
    buffer: BytesIO = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _, height = A4

    font_path: str = "C:/Windows/Fonts/arial.ttf"
    bold_font_path: str = "C:/Windows/Fonts/arialbd.ttf"

    pdfmetrics.registerFont(TTFont("Arial", font_path))
    pdfmetrics.registerFont(TTFont("Arial-Bold", bold_font_path))

    y: int = int(height - 50)

    pdf.setFont("Arial-Bold", 16)
    pdf.drawString(50, y, f"Рахунок на оплату #{order.id}")
    y -= 35

    pdf.setFont("Arial", 11)
    pdf.drawString(50, y, "Клініка: Avelon Healthcare")
    y -= 20
    pdf.drawString(50, y, "ЄДРПОУ: 12345678")
    y -= 20
    pdf.drawString(50, y, "IBAN: UA123456789012345678901234567")
    y -= 20
    pdf.drawString(50, y, "Банк: АТ КБ Приклад Банк")
    y -= 20
    pdf.drawString(50, y, "МФО: 300001")
    y -= 35

    payer_name: str = order.full_name or order.customer_name

    pdf.setFont("Arial-Bold", 12)
    pdf.drawString(50, y, "Дані замовлення")
    y -= 25

    pdf.setFont("Arial", 11)
    pdf.drawString(50, y, f"Платник: {payer_name}")
    y -= 20
    pdf.drawString(50, y, f"Телефон: {order.phone}")
    y -= 20
    pdf.drawString(50, y, f"Email: {order.email}")
    y -= 20
    pdf.drawString(50, y, f"Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}")
    y -= 20
    pdf.drawString(50, y, f"Спосіб оплати: {order.get_payment_method_display()}")
    y -= 20
    pdf.drawString(50, y, f"Сума: {order.total_price} грн")
    y -= 35

    pdf.setFont("Arial-Bold", 12)
    pdf.drawString(50, y, "Перелік аналізів")
    y -= 25

    pdf.setFont("Arial-Bold", 10)
    pdf.drawString(50, y, "Назва аналізу")
    pdf.drawString(340, y, "Термін")
    pdf.drawString(440, y, "Ціна")
    y -= 15

    pdf.line(50, y, 550, y)
    y -= 20

    pdf.setFont("Arial", 10)

    for item in order.items.all():
        if y < 80:
            pdf.showPage()
            pdf.setFont("Arial", 10)
            y = int(height - 50)

        pdf.drawString(50, y, str(item.analysis.name)[:45])
        pdf.drawString(340, y, f"{item.analysis.duration_days} дн.")
        pdf.drawString(440, y, f"{item.price} грн")
        y -= 20

    y -= 10
    pdf.line(50, y, 550, y)
    y -= 25

    pdf.setFont("Arial-Bold", 12)
    pdf.drawString(340, y, "Разом:")
    pdf.drawString(440, y, f"{order.total_price} грн")

    pdf.showPage()
    pdf.save()

    pdf_bytes: bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def build_order_invoice_response(order: Order) -> HttpResponse:
    """
    Повертає HTTP-відповідь з PDF-рахунком.

    Args:
        order (Order): Замовлення.

    Returns:
        HttpResponse: PDF-відповідь.
    """
    pdf_bytes: bytes = generate_order_invoice_pdf(order)
    response: HttpResponse = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice_order_{order.id}.pdf"'
    return response


def send_order_email(order: Order) -> None:
    """
    Надсилає лист із даними замовлення.

    Args:
        order (Order): Замовлення.

    Returns:
        None
    """
    context: dict[str, object] = {
        "order": order,
        "online_payment_links": {
            "Portmone": "https://www.portmone.com.ua/",
            "EasyPay": "https://easypay.ua/ua",
            "iPay": "https://ipay.ua/",
            "Masterpass": "https://www.mastercard.ua/",
        },
    }

    html_body: str = render_to_string(
        "avelon_healthcare/orders/order_email.html",
        context,
    )

    attachments: list[tuple[str, bytes, str]] = []

    if order.payment_method in {PaymentMethod.BANK_TRANSFER, PaymentMethod.ONLINE}:
        invoice_pdf: bytes = generate_order_invoice_pdf(order)
        attachments.append(
            (
                f"invoice_order_{order.id}.pdf",
                invoice_pdf,
                "application/pdf",
            )
        )

    send_html_email(
        subject=f"Avelon Healthcare — замовлення #{order.id}",
        html_body=html_body,
        to=[order.email],
        attachments=attachments,
    )