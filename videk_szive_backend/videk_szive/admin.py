from django.contrib import admin
from .models import Guest,Room,Reservation

# Register your models here.

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Szoba adatok", {
            "fields": (
                "room_number",
                "room_type",
                "room_persons",
                "room_size",
                "balcony",
                "price_per_night",
            ),
        }),
        ("Státusz", {
            "fields": (
                "status_free",
                "status_booked",
                "status_need_cleaning",
                "status_under_cleaning",
                "status_cleaned",
            ),
        }),
        ("Takarítási igények", {
            "fields": (
                "cleaning",
                "not_cleaning",
                "extra_sheets",
                "extra_towel",
                "extra_showers",
                "bin_clean",
                "wake_up",
                "issues",
            ),
        }),
        ("Egyebek", {
            "fields": (
                "wifi",
                "current_guest",
            ),
        }),
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "guest",
        "room",
        "arrive_date",
        "leave_date",
        "adult_number",
        "kid_number",
    )

    list_filter = (
        "arrive_date",
        "leave_date",
    )

    search_fields = (
        "guest__guest_name",
        "room__room_number",
    )