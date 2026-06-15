from django.contrib import admin
from django.urls import path
from videk_szive.views import room_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path("room/<int:room_number>/", room_detail, name="room_detail"),
]
