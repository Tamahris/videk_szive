from django.contrib import admin
from django.urls import path
from videk_szive import views
from videk_szive.views import version #

urlpatterns = [
    path('', views.home, name='home'),
    path("room/<int:room_number>/", views.room_detail, name="room_detail"),
    path("info/", views.room_info, name="room_info"),
    path('takaritas/', views.cleaner_dashboard, name='cleaner_dashboard'),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("version/", version), #
    path('summary/', views.summary, name='summary'),
    path('needclean/', views.need_clean, name='need_clean'),
    path('extras/', views.extras, name='extras'),
    path('progress/', views.progress, name = 'progress'),
    path('update-cleaning/<int:room_number>/', views.update_cleaning, name='update_cleaning'),
    path('handyman/', views.handyman_dashboard, name='handyman_dashboard'),
    path('issue/<int:issue_id>/resolve/', views.resolve_issue, name='resolve_issue'),
    path('issue/<int:issue_id>/update-note/', views.update_issue_note, name='update_issue_note'),
    path('reception/', views.reception_dashboard, name='reception'),
    path('room/<int:room_number>/confirm-wakeup/', views.confirm_wake_up, name='confirm_wake_up'),
    path('room/<int:room_number>/complete-wakeup/', views.complete_wake_up, name='complete_wake_up'),
    path('check-in/', views.checkin_view, name='checkin_view'),
    path('reception/check-out/', views.checkout_view, name='checkout_view'),
    path('szobak/', views.all_rooms_view, name='all_rooms'),
    path('takaritasok/', views.cleaning_history_view, name='cleaning_history'),
    path('karbantartasok/', views.issue_history_view, name='issue_history'),
    path('online-foglalasok/', views.online_reservation_view, name='online_foglalasok'),
]