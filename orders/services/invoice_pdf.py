from __future__ import annotations
from io import BytesIO
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from orders.models import Order


def _register_fonts() -> None:
    """
    Реєструє шрифти для генерації PDF.

    Returns:
        None
    """
    fonts_dir = Path(settings.BASE_DIR) / "static" / "fonts"

    regular_font_path = fonts_dir / "DejaVuSans.ttf"
    bold_font_path = fonts_dir / "DejaVuSans-Bold.ttf"

    pdfmetrics.registerFont(TTFont("DejaVuSans", str(regular_font_path)))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(bold_font_path)))


def generate_order_invoice_pdf(order: Order) -> bytes:
    """
    Генерує PDF-рахунок для замовлення.

    Args:
        order: Замовлення, для якого формується рахунок.

    Returns:
        bytes: Вміст PDF-файлу.
    """
    _register_fonts()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _, height = A4

    y = int(height - 50)

    pdf.setFont("DejaVuSans-Bold", 16)
    pdf.drawString(50, y, f"Рахунок на оплату #{order.id}")
    y -= 35

    pdf.setFont("DejaVuSans", 11)
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

    payer_name = order.full_name or order.customer_name

    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(50, y, "Дані замовлення")
    y -= 25

    pdf.setFont("DejaVuSans", 11)
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

    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(50, y, "Перелік аналізів")
    y -= 25

    pdf.setFont("DejaVuSans-Bold", 10)
    pdf.drawString(50, y, "Назва аналізу")
    pdf.drawString(340, y, "Термін")
    pdf.drawString(440, y, "Ціна")
    y -= 15

    pdf.line(50, y, 550, y)
    y -= 20

    pdf.setFont("DejaVuSans", 10)

    for item in order.items.all():
        if y < 80:
            pdf.showPage()
            pdf.setFont("DejaVuSans", 10)
            y = int(height - 50)

        pdf.drawString(50, y, str(item.analysis.name)[:45])
        pdf.drawString(340, y, f"{item.analysis.duration_days} дн.")
        pdf.drawString(440, y, f"{item.price} грн")
        y -= 20

    y -= 10
    pdf.line(50, y, 550, y)
    y -= 25

    pdf.setFont("DejaVuSans-Bold", 12)
    pdf.drawString(340, y, "Разом:")
    pdf.drawString(440, y, f"{order.total_price} грн")

    pdf.showPage()
    pdf.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def build_order_invoice_response(order: Order) -> HttpResponse:
    """
    Формує HTTP-відповідь з PDF-рахунком замовлення.

    Args:
        order: Замовлення, для якого формується відповідь.

    Returns:
        HttpResponse: Відповідь з PDF-файлом.
    """
    pdf_bytes = generate_order_invoice_pdf(order)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice_order_{order.id}.pdf"'
    return response
