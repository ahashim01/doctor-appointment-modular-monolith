from django.urls import path

from appointment_management.adapters.inbound.controllers import (
    CancelAppointmentController,
    MarkAppointmentCompletedController,
    UpcomingAppointmentsController,
)

urlpatterns = [
    path("upcoming/", UpcomingAppointmentsController.as_view(), name="upcoming-appointments"),
    path(
        "<uuid:appointment_id>/complete/",
        MarkAppointmentCompletedController.as_view(),
        name="mark-appointment-completed",
    ),
    path("<uuid:appointment_id>/cancel/", CancelAppointmentController.as_view(), name="cancel-appointment"),
]
