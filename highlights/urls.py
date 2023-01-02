from django.urls import path

from highlights import views

app_name = "highlights"

urlpatterns = [
    path("", views.List.as_view(), name="list"),
    path("highlight-list/", views.SearchViewAPI.as_view(), name="highlight-list"),
    path("add/", views.Add.as_view(), name="add"),
    path("<str:pk>/edit/", views.Edit.as_view(), name="edit"),
    path("<str:pk>/confirm-delete/", views.confirm_delete, name="confirm-delete"),
    path("<str:pk>/delete/", views.delete, name="delete"),
]
