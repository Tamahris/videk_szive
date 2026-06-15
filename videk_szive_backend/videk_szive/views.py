from django.shortcuts import render, get_object_or_404, redirect
from .models import Room

def room_detail(request, room_number):

    room = get_object_or_404(Room, room_number=room_number)

    if request.method == "POST":

        if room.room_number == 101:

            action = request.POST.get("action")

            if action == "cleaning":
                room.cleaning = True

            elif action == "not_cleaning":
                room.not_cleaning = True

            elif action == "extra_sheets":
                room.extra_sheets = True

            elif action == "extra_towel":
                room.extra_towel = True

            elif action == "extra_showers":
                room.extra_showers = True

            elif action == "bin_clean":
                room.bin_clean = True

            elif action == "wake_up":
                room.wake_up = True

            elif action == "issues":
                room.issues = True

            room.save()

        return redirect("room_detail", room_number=room_number)
    
    

    return render(request, "room.html", {"room": room})