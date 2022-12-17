from django.shortcuts import render
from django.views import generic


from highlights import models

# Create your views here.
def highlights_list(request):
    highlights = handle_search(request)

    return render(request, 'highlights/list.html', {"highlights": highlights})


class SearchViewAPI(generic.View):

    def get(self, request):
        highlights = handle_search(request)
        return render(request, "highlights/partials/highlight-list.html", {"highlights": highlights})
        
def handle_search(request):
    search_text = request.GET.get("query")
    highlights = models.Highlight.objects.all()
    if search_text:
        highlights = highlights.filter(text__icontains=search_text)
    return highlights