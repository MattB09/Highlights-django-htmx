from django.urls import path

from highlights.views import highlights, tags

app_name = "highlights"

urlpatterns = [
    path("", highlights.List.as_view(), name="list"),
    path("highlight-list/", highlights.HxSearchView.as_view(), name="highlight-list"),
    path("add/", highlights.Add.as_view(), name="add"),
    path("<str:pk>/edit/", highlights.Edit.as_view(), name="edit"),
    path("<str:pk>/confirm-delete/", highlights.confirm_delete, name="confirm-delete"),
    path("<str:pk>/delete/", highlights.delete, name="delete"),
    path("tags/add/", tags.Add.as_view(), name="tag-add"),
]
