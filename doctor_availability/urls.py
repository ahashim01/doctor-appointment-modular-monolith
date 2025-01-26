from django.urls import path

from .views import SlotListCreateView

urlpatterns = [
    path("slots/", SlotListCreateView.as_view(), name="slot-list-create"),
]
