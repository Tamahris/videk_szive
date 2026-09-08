from django.contrib import admin
from .models import Guest,RoomIssue,Room,Reservation,CleaningTask

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass

@admin.register(RoomIssue)
class RoomIssueAdmin(admin.ModelAdmin):
    list_display = ('room', 'description', 'is_resolved', 'created_at', 'resolved_at')
    list_filter = ('is_resolved',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number', 'room_type', 'status_free', 'status_booked', 
        'status_need_cleaning', 'wake_up', 'wake_up_time', 'wake_up_confirmed', 'issues'
    )

    list_filter = (
        'room_type', 'status_free', 'status_booked', 
        'status_need_cleaning', 'wake_up', 'wake_up_confirmed', 'issues'
    )
    
    search_fields = ('room_number', 'wifi')
    
    list_editable = ('status_free', 'status_booked', 'status_need_cleaning', 'wake_up_confirmed')

    fieldsets = (
        ("Általános Szoba Adatok", {
            "fields": ("room_number", "room_type", "room_persons", "room_size", "price_per_night", "balcony", "wifi", "current_guest")
        }),
        ("Rendszer Státuszok", {
            "fields": ("status_free", "status_booked", "status_need_cleaning", "status_under_cleaning", "status_cleaned", "issues", "issue_description")
        }),
        ("Takarítási és Extra Igények", {
            "fields": ("cleaning", "not_cleaning", "extra_sheets", "extra_towel", "extra_showers", "bin_clean")
        }),
        ("⏰ Ébresztési Kérések", {
            "fields": ("wake_up", "wake_up_time", "wake_up_confirmed"),
            "description": "A vendég által leadott aktív reggeli ébresztések és azok recepciós státusza."
        }),
    )
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "guest",
        "room",
        "room_type",
        "status",
        "arrive_date",
        "leave_date",
        "adult_number",
        "kid_number",
    )

    list_filter = (
        "status",
        "arrive_date",
        "leave_date",
    )

    search_fields = (
        "guest__guest_name",
        "room__room_number",
    )

@admin.register(CleaningTask)
class CleaningTaskAdmin(admin.ModelAdmin):
    list_display = ('room', 'status', 'started_at', 'finished_at', 'cleaner', 'created_at')
    
    list_filter = ('status', 'cleaner', 'room')
    
    search_fields = ('room__room_number', 'cleaner__username')

