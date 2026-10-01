from datetime import date, datetime

from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import Booking


def home(request):
    return render(request, 'home/index.html')


def booking(request):

    if request.method == 'POST':

        booking_date = request.POST.get('date')
        booking_time = request.POST.get('time')

        # Validate date
        try:
            selected_date = date.fromisoformat(booking_date)
        except (ValueError, TypeError):
            return render(request, 'home/booking.html', {
                'error': 'Please select a valid date.',
                'today': date.today().isoformat()
            })

        # Prevent previous dates
        if selected_date < date.today():
            return render(request, 'home/booking.html', {
                'error': 'You cannot book a date in the past.',
                'today': date.today().isoformat()
            })

        # Prevent past time if booking is today
        if selected_date == date.today():

            try:
                selected_datetime = datetime.strptime(
                    f"{booking_date} {booking_time}",
                    "%Y-%m-%d %H:%M"
                )

                if selected_datetime < datetime.now():
                    return render(request, 'home/booking.html', {
                        'error': 'Please select a future time.',
                        'today': date.today().isoformat()
                    })

            except (ValueError, TypeError):
                return render(request, 'home/booking.html', {
                    'error': 'Please select a valid time.',
                    'today': date.today().isoformat()
                })

        # Save booking
        booking = Booking.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            date=booking_date,
            time=booking_time,
            guests=request.POST.get('guests'),
            special_request=request.POST.get('message'),
        )

        # Send confirmation email to customer
        send_mail(
            subject='Olive Cafe - Booking Confirmation',
            message=f"""
Hello {booking.name},

Your booking at Olive Cafe has been confirmed.

Booking Details:
-------------------------
Date: {booking.date}
Time: {booking.time}
Guests: {booking.guests}
Phone: {booking.phone}

Special Request:
{booking.special_request or 'None'}

Thank you for choosing Olive Cafe!

We look forward to welcoming you.

Olive Cafe
""",
            from_email=None,
            recipient_list=[booking.email],
            fail_silently=False,
        )

        # Send notification email to Olive Cafe
        send_mail(
            subject='Olive Cafe - New Booking Received',
            message=f"""
New booking received at Olive Cafe.

Booking Details:
-------------------------
Name: {booking.name}
Email: {booking.email}
Phone: {booking.phone}
Date: {booking.date}
Time: {booking.time}
Guests: {booking.guests}

Special Request:
{booking.special_request or 'None'}

Please check the Django Admin for more details.

Olive Cafe
""",
            from_email=None,
            recipient_list=['olivecafe5251@gmail.com'],
            fail_silently=False,
        )

        return redirect('booking_success')

    return render(request, 'home/booking.html', {
        'today': date.today().isoformat()
    })


def booking_success(request):
    return render(request, 'home/booking_success.html')