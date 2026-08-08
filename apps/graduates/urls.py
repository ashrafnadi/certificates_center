from django.urls import path
from . import views

app_name = "graduates"

urlpatterns = [
    path("", views.index, name="index"),
    path("graduates/", views.graduate_list, name="graduate_list"),
    path("auditor/", views.auditor_graduate_list, name="auditor_list"),
    path(
        "auditor/toggle-check/<int:graduate_id>/",
        views.auditor_toggle_check,
        name="auditor_toggle_check",
    ),
    path(
        "auditor/update-notes/<int:graduate_id>/",
        views.auditor_update_notes,
        name="auditor_update_notes",
    ),
]
