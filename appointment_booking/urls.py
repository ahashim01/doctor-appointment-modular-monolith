from django.urls import path

from appointment_booking.interface_adapters.controllers import BookAppointmentController

urlpatterns = [
    path("book/", BookAppointmentController.as_view(), name="book-appointment"),
]
