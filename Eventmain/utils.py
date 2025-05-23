import qrcode
from django.conf import settings
import os

def generate_qr_for_booking(booking):
    data = f'BookingID:{booking.id}|User:{booking.user.id}|Ticket:{booking.ticket.id}'
    img = qrcode.make(data)
    filename = f'qr_{booking.id}.png'
    path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return f'/media/qrcodes/{filename}'
