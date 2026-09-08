from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from videk_szive.models import Room, Reservation, Guest
from django.utils import timezone


def fooldal_view(request):
    return render(request, 'website/fooldal.html')
def szallas_view(request): 
    return render(request, 'website/szallas.html')
def wellness_view(request): 
    return render(request, 'website/wellness.html')
def etterem_view(request): 
    return render(request, 'website/etterem.html')
def galeria_view(request): 
    return render(request, 'website/galery.html')
def kapcsolat_view(request): 
    return render(request, 'website/kapcsolat.html')
def foglalas_view(request): 
    return render(request, 'website/reservation.html')

def foglalas_view(request):
    if request.method == 'POST':
        guest_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        check_in_str = request.POST.get('check_in')   
        check_out_str = request.POST.get('check_out') 
        room_type = request.POST.get('room_type')
        
        adults = int(request.POST.get('adults', 1))
        kids = int(request.POST.get('kids', 0))

        if not check_in_str or not check_out_str:
            messages.error(request, "Kérjük válassza ki az érkezési és távozási dátumot a naptárban!")
            room_types = Room.objects.values_list('room_type', flat=True).distinct()
            return render(request, 'website/foglalas.html', {'room_types': room_types})

        try:
            arrive_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            leave_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Érvénytelen dátum formátum!")
            room_types = Room.objects.values_list('room_type', flat=True).distinct()
            return render(request, 'website/foglalas.html', {'room_types': room_types})

        today = timezone.now().date()
        max_date = today.replace(year=today.year + 1)

        if arrive_date < today:
            messages.error(
                request, "Múltbeli dátumra nem lehetséges a foglalás!"
            )
            room_types = Room.objects.values_list(
                "room_type", flat=True
            ).distinct()
            return render(
                request, "website/foglalas.html", {"room_types": room_types}
            )

        if leave_date <= arrive_date:
            messages.error(
                request,
                "A távozás dátumának későbbre kell esnie, mint az érkezés"
                " dátuma!",
            )
            room_types = Room.objects.values_list(
                "room_type", flat=True
            ).distinct()
            return render(
                request, "website/foglalas.html", {"room_types": room_types}
            )

        if arrive_date > max_date:
            messages.error(
                request,
                "Legfeljebb 1 évre előre fogadunk online foglalásokat!",
            )
            room_types = Room.objects.values_list(
                "room_type", flat=True
            ).distinct()
            return render(
                request, "website/foglalas.html", {"room_types": room_types}
            )

        selected_room = Room.objects.filter(room_type=room_type).first()

        if not selected_room:
            messages.error(request, "Sajnos a megadott szobatípus jelenleg nem elérhető.")
            room_types = Room.objects.values_list('room_type', flat=True).distinct()
            return render(request, 'website/foglalas.html', {'room_types': room_types})

        guest = Guest.objects.filter(email=email).first()

        if not guest:
            guest = Guest.objects.create(
                guest_name=guest_name,
                email=email,
                phone_number=phone,
                birth_date='2000-01-01', 
                personal_id=f"ONLINE-{int(datetime.now().timestamp())}"
            )
        else:
            guest.guest_name = guest_name
            guest.phone_number = phone
            guest.save()

        Reservation.objects.create(
            guest=guest,
            room=None,
            room_type=room_type,  
            arrive_date=arrive_date,
            leave_date=leave_date,
            adult_number=adults,
            kid_number=kids,
            comment="Online weboldali foglalás"
        )
        
        messages.success(request, "Köszönjük! Foglalási igényét sikeresen rögzítettük. Munkatársunk hamarosan felveszi Önnel a kapcsolatot.")
        return redirect('foglalas')

    room_types = Room.objects.values_list('room_type', flat=True).distinct()
    return render(request, 'website/foglalas.html', {'room_types': room_types})
