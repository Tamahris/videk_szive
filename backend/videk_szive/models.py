from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Guest(models.Model):
    guest_name = models.CharField(max_length=100, verbose_name="Vendég neve")
    birth_date = models.DateField(verbose_name="Születési dátum")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefonszám")
    personal_id = models.CharField(max_length=20, unique=True, verbose_name="Személyi igazolvány szám")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail cím")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lakcím")
    
    class Meta:
        verbose_name_plural = "Guests"
        
    def __str__(self):
        return f"{self.guest_name} ({self.personal_id})"

class Room(models.Model):

    room_number = models.IntegerField(primary_key=True, verbose_name="Szobaszám")
    room_type = models.CharField(max_length=50, verbose_name="Szobatípus")
    room_persons = models.IntegerField(verbose_name="Férőhely")
    room_size = models.IntegerField(verbose_name="Szobaméret (m²)")
    balcony = models.BooleanField(default=False, verbose_name="Erkélyes")
    price_per_night = models.IntegerField(verbose_name="Ár/éjszaka")

    status_free = models.BooleanField(default=True, verbose_name="Szabad szoba")
    status_booked = models.BooleanField(default=False, verbose_name="Kiadott szoba")
    status_need_cleaning = models.BooleanField(default=False, verbose_name="Takarítandó szoba")
    status_under_cleaning = models.BooleanField(default=False, verbose_name="Takarítás alatt álló szoba")
    status_cleaned = models.BooleanField(default=False, verbose_name="Kitakarított szoba")

    cleaning = models.BooleanField(default=False, verbose_name="Takarítást kér")
    not_cleaning = models.BooleanField(default=False, verbose_name="Takarítást nem kér")
    extra_sheets = models.BooleanField(default=False, verbose_name="Extra ágynemű")
    extra_towel = models.BooleanField(default=False, verbose_name="Extra törölköző")
    extra_showers = models.BooleanField(default=False, verbose_name="Extra tusfürdő")
    bin_clean = models.BooleanField(default=False, verbose_name="Szemetes ürítés")
    wake_up = models.BooleanField(default=False, verbose_name="Ébresztés kérése")
    wake_up_time = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ébresztési időpont / Megjegyzés")
    wake_up_confirmed = models.BooleanField(default=False, verbose_name="Ébresztés visszaigazolva")
    issues = models.BooleanField(default=False, verbose_name="Műszaki hiba")
    issue_description = models.TextField(blank=True, null=True)

  

    wifi = models.CharField(max_length=50, blank=True, null=True, verbose_name="Wi-Fi jelszó")
    
    current_guest = models.ForeignKey(
        Guest, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name="rooms",
        verbose_name="Aktuális vendég"
    )

    class Meta:
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.room_number}. szoba ({self.room_type})"
    
class RoomIssue(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reported_issues")
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    handyman_note = models.TextField(blank=True, null=True, verbose_name="Karbantartó megjegyzése")
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="Megoldás ideje")

    def __str__(self):
        status = "Kész" if self.is_resolved else "Aktív"
        return f"{self.room.room_number} - {self.description[:30]}... ({status})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Feldolgozásra vár'),
        ('CONFIRMED', 'Visszaigazolva / Check-inre vár'),
        ('CHECKED_IN', 'Bejelentkezett'),
        ('CHECKED_OUT', 'Kijelentkezett'),
    ]
    
    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Vendég"
    )

    room = models.ForeignKey(Room,on_delete=models.SET_NULL, related_name="reservations", verbose_name="Szoba", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Státusz")
    room_type = models.CharField(max_length=50, null=True, blank=True, verbose_name="Szobatípus")
    arrive_date = models.DateField(verbose_name="Érkezés dátuma")
    leave_date = models.DateField(verbose_name="Távozás dátuma")
    adult_number = models.IntegerField(default=1, verbose_name="Felnőttek száma")
    kid_number = models.IntegerField(default=0, verbose_name="Gyerekek száma")
    comment = models.TextField(blank=True, null=True, verbose_name="Megjegyzés")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reservations"

    def __str__(self):
        room_display = self.room.room_number if self.room else "Beosztásra vár"
        return f"{self.guest} - {room_display} ({self.arrive_date} - {self.leave_date})"
        

class CleaningTask(models.Model):
    STATUS_CHOICES = [
        ("needed", "Szükséges"),
        ("in_progress", "Folyamatban"),
        ("done", "Kész"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="cleanings")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="needed")

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    cleaner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)