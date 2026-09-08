from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Room, RoomIssue, Guest, Reservation, CleaningTask
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime
import videk_szive.state as state
from django.http import JsonResponse

@login_required  
def room_detail(request, room_number):

    username = request.user.username
    try:
        room_number = int(request.user.username)
    except ValueError:
        raise Http404("Nincs hozzárendelt szoba ehhez a userhez")
        
    room = get_object_or_404(Room, room_number=room_number)
    
    try:
        reservation = Reservation.objects.filter(room=room, status='CHECKED_IN').first()
        
        if reservation:
            guest = reservation.guest
        else:
            guest = None
    except Exception:
        reservation = None
        guest = None
        
    active_issues = room.reported_issues.filter(is_resolved=False).order_by('-created_at')
    
    return render(request, "room.html", {
        "room_number": room_number, 
        "room": room,               
        "reservation": reservation, 
        "guest": guest,             
        "active_issues": active_issues 
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.username.isdigit():
                return redirect("home")
            elif user.username == "karbantarto":
                return redirect("handyman_dashboard")
            elif user.username == "recepcio":
                return redirect("reception")
            else:
                return redirect("summary")
        else:
            messages.error(request, "Hibás felhasználónév vagy jelszó!")
            return redirect("login")
    return render(request, "welcome.html")

def home(request):
    if request.user.is_authenticated:
        room_number_str = request.user.username
        if room_number_str.isdigit():
            room_number = int(room_number_str)
            room = get_object_or_404(Room, room_number=room_number)
            if request.method == "POST":
                action = request.POST.get("action")
                if action == "save_services":
                    cleaning_requested = "cleaning" in request.POST
                    room.cleaning = cleaning_requested
                    room.status_need_cleaning = cleaning_requested
                    room.extra_sheets = "extra_sheets" in request.POST
                    room.extra_towel = "extra_towel" in request.POST
                    room.extra_showers = "extra_showers" in request.POST
                    room.bin_clean = "bin_clean" in request.POST
                    wake_up_text = request.POST.get("wake_up", "").strip()
                    if wake_up_text:
                        room.wake_up = True
                        room.wake_up_time = wake_up_text
                        room.wake_up_confirmed = False
                    else:
                        room.wake_up = False
                        room.wake_up_time = ""
                        room.wake_up_confirmed = False
                    room.save()
                    state.VERSION += 1
                    new_issue_text = request.POST.get("new_issue", "").strip()
                    if new_issue_text:
                        RoomIssue.objects.create(room=room, description=new_issue_text)
                    messages.success(request, "Igényei sikeresen továbbítva a recepcióra!")
                    return redirect("home")
            try:
                reservation = Reservation.objects.filter(room=room,status='CHECKED_IN').first()
                guest = reservation.guest if reservation else None
            except Exception:
                reservation = None
                guest = None
            active_issues = room.reported_issues.filter(is_resolved=False).order_by('-created_at')
            return render(request, "room.html", {
                "room_number": room_number,
                "room": room,
                "reservation": reservation,
                "guest": guest,
                "active_issues": active_issues
            })
    return render(request, "welcome.html")

@login_required  
def room_info(request):
    username = request.user.username
    return render(request, "info.html", {"room_number": username})

def logout_view(request):
    storage = get_messages(request)
    for message in storage:
        pass
    logout(request)
    return redirect("home")

def cleaner_dashboard(request):
    rooms = Room.objects.all().order_by('room_number')
    return render(request, 'cleaner.html', {'rooms': rooms})

def version(request):
    return JsonResponse({"version": state.VERSION})

@login_required  
def summary(request):

    context = {
        "cleaning_count": Room.objects.filter(Q(cleaning=True) | Q(status_need_cleaning=True)).distinct().count(),
        "sheets_count": Room.objects.filter(extra_sheets=True).count(),
        "towel_count": Room.objects.filter(extra_towel=True).count(),
        "shower_count": Room.objects.filter(extra_showers=True).count(),
        "bin_count": Room.objects.filter(bin_clean=True).count(),
    }
    return render(request, "summary.html", context)

@login_required 
def need_clean(request):
    rooms = Room.objects.filter(status_need_cleaning=True).order_by('room_number')
    return render(request, "needclean.html", {"rooms": rooms})

@login_required  
def extras(request):
    rooms = Room.objects.filter(
        Q(extra_sheets=True)  |
        Q(extra_towel=True) |
        Q(extra_showers=True) |
        Q(bin_clean=True)
        ).distinct().order_by('room_number')
    return render(request, "extras.html", {"rooms": rooms})

@login_required  
def progress(request):
    rooms = Room.objects.filter(status_under_cleaning=True).order_by('room_number')
    return render(request, "progress.html", {"rooms": rooms})

@require_POST  
@login_required  
def update_cleaning(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    now = timezone.now()
    task = CleaningTask.objects.filter(
        room=room,
        status__in=["needed", "in_progress"]
    ).first()
    if not task and (room.status_need_cleaning or room.cleaning):
        task = CleaningTask.objects.create(
            room=room,
            status="needed"
        )
    if task:
        if task.status == "needed":
            task.status = "in_progress"
            task.started_at = now
            task.cleaner = request.user
            task.save()
            state.VERSION += 1
            room.status_need_cleaning = False
            room.status_under_cleaning = True
            room.save()
            state.VERSION += 1
            return redirect(request.META.get('HTTP_REFERER', 'need_clean'))

        elif task.status == "in_progress":
            task.status = "done"
            task.finished_at = now
            task.save()
            state.VERSION += 1
            room.status_under_cleaning = False
            room.status_cleaned = True
            room.cleaning = False
            room.extra_sheets = False
            room.extra_towel = False
            room.extra_showers = False
            room.bin_clean = False
            room.save()
            state.VERSION += 1
            return redirect(request.META.get('HTTP_REFERER', 'need_clean'))
    CleaningTask.objects.create(
        room=room,
        status="done",
        started_at=now,
        finished_at=now,
        cleaner=request.user
    )
    room.extra_sheets = False
    room.extra_towel = False
    room.extra_showers = False
    room.bin_clean = False
    room.save()

    state.VERSION += 1
    return redirect(request.META.get('HTTP_REFERER', 'need_clean'))

@login_required  
def handyman_dashboard(request):
    active_issues = RoomIssue.objects.filter(is_resolved=False).order_by('room__room_number')
    return render(request, 'handyman.html', {'issues': active_issues})

@require_POST  
@login_required  
def resolve_issue(request, issue_id):
    issue = get_object_or_404(RoomIssue, id=issue_id)
    issue.is_resolved = True
    issue.resolved_at = timezone.now()
    issue.save()
    state.VERSION += 1
    room = issue.room
    if not room.reported_issues.filter(is_resolved=False).exists():
        room.issues = False
        room.save()
        state.VERSION += 1
    messages.success(request, f"A(z) {room.room_number}. szoba hibája elhárítva!")
    return redirect('handyman_dashboard')

@require_POST  
@login_required  
def update_issue_note(request, issue_id):
    issue = get_object_or_404(RoomIssue, id=issue_id)
    note = request.POST.get('handyman_note', '').strip()
    issue.handyman_note = note
    issue.save()
    state.VERSION += 1
    messages.success(request,f"A(z) {issue.room.room_number}. szoba státusza frissítve!")
    return redirect('handyman_dashboard')

@login_required 
def reception_dashboard(request):
    rooms = Room.objects.all().order_by('room_number')
    wake_up_rooms = Room.objects.filter(wake_up=True).order_by('room_number')
    free_rooms_count = Room.objects.filter(status_free=True).count()
    booked_rooms_count = Room.objects.filter(status_booked=True).count()
    clean_need_count = Room.objects.filter(status_need_cleaning=True).count()
    clean_under_count = Room.objects.filter(status_under_cleaning=True).count()
    today = timezone.localdate()
    arrivals = Reservation.objects.filter(arrive_date=today, status__in=['PENDING', 'CONFIRMED']).select_related('guest', 'room').order_by('id')
    checkout_reservations = Reservation.objects.filter(leave_date=today).select_related('guest','room').order_by('room__room_number')
    active_issues = RoomIssue.objects.filter(
        is_resolved=False).select_related('room').order_by('room__room_number')
    context = {
        'rooms': rooms,
        'wake_up_rooms': wake_up_rooms,
        'free_count': free_rooms_count,
        'booked_count': booked_rooms_count,
        'need_cleaning_count': clean_need_count,
        'under_cleaning_count': clean_under_count,
        'arrivals': arrivals,
        'checkout_reservations': checkout_reservations,
        'active_issues': active_issues,
    }
    return render(request, 'reception.html', context)

@require_POST  
@login_required 
def confirm_wake_up(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    room.wake_up_confirmed = True
    room.save()
    state.VERSION += 1
    messages.success(request, f"A(z) {room.room_number}. szoba ébresztési kérése visszaigazolva!")
    return redirect(request.META.get('HTTP_REFERER', 'reception'))

@require_POST  
@login_required 
def complete_wake_up(request, room_number):

    room = get_object_or_404(Room, room_number=room_number)
    room.wake_up = False
    room.wake_up_time = ""
    room.wake_up_confirmed = False
    room.save()
    state.VERSION += 1
    messages.success(request,f"A(z) {room.room_number}. szoba ébresztése sikeresen végrehajtva és lezárva!")
    return redirect(request.META.get('HTTP_REFERER', 'reception'))

def checkin_view(request):
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        room_type = request.POST.get('room_type')
        birth_date = request.POST.get('birth_date')
        phone_number = request.POST.get('phone_number')
        personal_id = request.POST.get('personal_id')
        email = request.POST.get('email')
        address = request.POST.get('address')
        arrive_date = request.POST.get('arrive_date')
        leave_date = request.POST.get('leave_date')
        adult_number = request.POST.get('adult_number', 1)
        kid_number = request.POST.get('kid_number', 0)
        comment = request.POST.get('comment')
        selected_room_number = request.POST.get('selected_room')

        try:
            room = Room.objects.get(room_number=selected_room_number)
        except Room.DoesNotExist:
            messages.error(request,"Hiba: A kiválasztott szoba nem található!")
            return redirect(request.path)

        guest, created = Guest.objects.get_or_create(
            personal_id=personal_id,
            defaults={
                'guest_name': guest_name,
                'birth_date': birth_date,
                'phone_number': phone_number,
                'email': email,
                'address': address
            }
        )

        if not created:
            guest.guest_name = guest_name
            guest.phone_number = phone_number
            guest.email = email
            guest.address = address
            guest.save()
            state.VERSION += 1

        reservation_id = request.GET.get('reservation_id')

        if reservation_id:
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.guest = guest
            reservation.room = room
            reservation.room_type = room.room_type
            reservation.arrive_date = arrive_date
            reservation.leave_date = leave_date
            reservation.adult_number = int(adult_number)
            reservation.kid_number = int(kid_number)
            reservation.comment = comment
            reservation.status = 'CHECKED_IN'
            reservation.save()
            state.VERSION += 1
        else:
            Reservation.objects.create(
                guest=guest,
                room=room,
                room_type=room.room_type,
                arrive_date=arrive_date,
                leave_date=leave_date,
                adult_number=int(adult_number),
                kid_number=int(kid_number),
                comment=comment,
                status='CHECKED_IN'
            )

        room.current_guest = guest
        room.status_free = False
        room.status_booked = True
        room.save()
        state.VERSION += 1

        available_rooms = Room.objects.filter(status_free=True)

        return render(request, 'check-in.html', {
            'available_rooms': available_rooms,
            'success': True
        })

    reservation_id = request.GET.get('reservation_id')
    prefilled_res = None

    if reservation_id:
        prefilled_res = Reservation.objects.filter(
            id=reservation_id
        ).select_related(
            'guest',
            'room'
        ).first()
    available_rooms = Room.objects.filter(status_free=True)
    return render(request, 'check-in.html', {
        'available_rooms': available_rooms,
        'res': prefilled_res
    })

@login_required
def checkout_view(request):

    if request.method == 'POST':
        room_number_raw = request.POST.get('room_number')
        
        if room_number_raw:
            
            room_number = int(room_number_raw)
            room = get_object_or_404(Room, room_number=room_number)
            
            active_reservation = Reservation.objects.filter(room=room, status='CHECKED_IN').first()
            
            if active_reservation:
                active_reservation.status = 'CHECKED_OUT'
                active_reservation.save()

            room.status_free = True        
            room.status_booked = False   
            room.current_guest = None    
            room.status_need_cleaning = True 
            
            room.wake_up = False        
            room.wake_up_time = None     
            room.wake_up_confirmed = False 
            room.cleaning = False          
            room.save()                    

            existing_task = CleaningTask.objects.filter(room=room, status__in=["needed", "in_progress"]).exists()
            
            if not existing_task:
                CleaningTask.objects.create(room=room, status="needed")

            state.VERSION += 1 

            booked_rooms = Room.objects.filter(status_booked=True).order_by('room_number')
            
            return render(request, 'check-out.html', {'booked_rooms': booked_rooms, 'success': True})

    booked_rooms = Room.objects.filter(status_booked=True).order_by('room_number')
    
    return render(request, 'check-out.html', {
        'booked_rooms': booked_rooms
    })

def all_rooms_view(request):
    rooms = Room.objects.all().select_related('current_guest').order_by('room_number')
    for room in rooms:
        if room.status_booked:
            room.active_reservation = Reservation.objects.filter(room=room).last()
        else:
            room.active_reservation = None

    context = {'rooms': rooms}
    return render(request, 'allrooms.html', context)

@login_required  
def cleaning_history_view(request):

    tasks = CleaningTask.objects.all().select_related('room','cleaner').order_by('-started_at')

    room_filter = request.GET.get('room_number','').strip()
    waiting_rooms = Room.objects.filter(status_need_cleaning=True)
    if room_filter:
        waiting_rooms = waiting_rooms.filter(room_number=room_filter)
    virtual_tasks = []
    for room in waiting_rooms:
        virtual_tasks.append(
            CleaningTask(
                room=room,
                status='needed',
                started_at=None
            )
        )

    if room_filter:
        tasks = tasks.filter(room__room_number=room_filter)

    start_date_str = request.GET.get('start_date','').strip()
    end_date_str = request.GET.get('end_date','').strip()
    if start_date_str:
        start_date = datetime.strptime(start_date_str,"%Y-%m-%d")
        tasks = tasks.filter(started_at__gte=start_date)
        if virtual_tasks:
            virtual_tasks = []

    if end_date_str:
        end_date = datetime.strptime(end_date_str,"%Y-%m-%d").replace( hour=23, minute=59, second=59)
        tasks = tasks.filter(started_at__lte=end_date)
        if virtual_tasks:
            virtual_tasks = []

    combined_tasks = list(virtual_tasks) + list(tasks)

    context = {
        'tasks': combined_tasks,
        'room_filter': room_filter,
        'start_date_filter': start_date_str,
        'end_date_filter': end_date_str,
    }
    return render(request,'cleaning_history.html',context)

@login_required 
def issue_history_view(request):
    issues = RoomIssue.objects.all().select_related('room').order_by('-created_at')
    room_filter = request.GET.get('room_number','').strip()

    if room_filter:
        issues = issues.filter(
            room__room_number=room_filter
        )

    start_date_str = request.GET.get('start_date','').strip()
    end_date_str = request.GET.get('end_date','').strip()

    if start_date_str:
        start_date = datetime.strptime(start_date_str,"%Y-%m-%d")
        issues = issues.filter(created_at__gte=start_date)
    if end_date_str:
        end_date = datetime.strptime(end_date_str,"%Y-%m-%d").replace( hour=23, minute=59, second=59)
        issues = issues.filter(created_at__lte=end_date)
    context = {
        'issues': issues,
        'room_filter': room_filter,
        'start_date_filter': start_date_str,
        'end_date_filter': end_date_str,
    }
    return render(request,'issue_history.html',context)

def online_reservation_view(request):

    pending_reservations = Reservation.objects.filter(room__isnull=True).order_by('-id')
    selected_id = request.GET.get('selected')
    selected_reservation = None
    if selected_id:
        selected_reservation = Reservation.objects.filter(id=selected_id, room__isnull=True).first()
    elif pending_reservations.exists():
        selected_reservation = pending_reservations.first()

    available_rooms = Room.objects.none()

    if selected_reservation:
        busy_room_ids = Reservation.objects.filter(
            room__isnull=False,
            status__in=['CONFIRMED', 'CHECKED_IN'],
            arrive_date__lt=selected_reservation.leave_date,
            leave_date__gt=selected_reservation.arrive_date
        ).values_list('room__room_number', flat=True) 

        available_rooms = Room.objects.exclude(room_number__in=busy_room_ids)

        req_type = selected_reservation.room_type
        if req_type and req_type.strip():
            available_rooms = available_rooms.filter(room_type__icontains=req_type.strip())
        else:
            available_rooms = Room.objects.none()

    if request.method == 'POST':
        action = request.POST.get('action')
        res_id = request.POST.get('reservation_id')
        if res_id:
            res = get_object_or_404(Reservation, id=res_id)
            if action == 'reject':
                guest_name = res.guest.guest_name
                guest_email = res.guest.email
                res.delete()
                state.VERSION += 1
                messages.warning(request, f"{guest_name} foglalása elutasítva. Értesítendő: {guest_email}")
                return redirect('online_foglalasok')
            elif action == 'accept':
                room_id = request.POST.get('room_id')
                if room_id:
                    room = get_object_or_404(Room, room_number=room_id)
                    res.room = room
                    res.status = 'CONFIRMED'
                    res.save()
                    state.VERSION += 1
                    messages.success(request, f"{res.guest.guest_name} foglalásához hozzárendelve a {room.room_number}. szoba!")
                    return redirect('online_foglalasok')

    context = {
        'pending_reservations': pending_reservations,
        'selected_reservation': selected_reservation,
        'all_rooms': available_rooms,
    }
    return render(request, 'online_reservation.html', context)