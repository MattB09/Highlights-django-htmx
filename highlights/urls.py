from django.urls import path

from highlights import views

app_name = 'highlights'

urlpatterns = [
    path("highlights/", views.highlights_list, name="list"),
    path("highlight-list/", views.SearchViewAPI.as_view(), name="highlight-list")
]