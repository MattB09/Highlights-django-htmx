from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse

from highlights import models
from highlights import forms


class List(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "highlights/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_text"] = self.request.GET.get("query", "")
        return context


class HxSearchView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Highlight
    template_name = "highlights/partials/highlight-list.html"
    context_object_name = "highlights"

    def get_queryset(self):
        query = self.request.GET.get("query")
        return models.Highlight.objects.search(self.request.user, query)


class Add(mixins.LoginRequiredMixin, generic.FormView):
    template_name = "highlights/add.html"
    form_class = forms.Highlight

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tags"] = models.Tag.objects.for_user(self.request.user)
        kwargs["books"] = models.Book.objects.for_user(self.request.user)
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        models.Highlight.new(
            text=form.cleaned_data["text"],
            book=form.cleaned_data["book"],
            tags=form.cleaned_data["tags"],
            user=self.request.user,
        )
        messages.add_message(self.request, messages.INFO, f"Highlight added!")
        return redirect("highlights:list")


class Edit(mixins.LoginRequiredMixin, generic.FormView):
    template_name = "highlights/edit.html"
    form_class = forms.Highlight

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.highlight = get_object_or_404(models.Highlight, pk=kwargs["pk"])

    def get_initial(self):
        initial = super().get_initial()
        initial["text"] = self.highlight.text
        initial["book"] = self.highlight.book
        initial["tags"] = self.highlight.tags.all()
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tags"] = models.Tag.objects.filter(user=self.request.user)
        kwargs["books"] = models.Book.objects.filter(user=self.request.user)
        kwargs["highlight_id"] = self.highlight.id
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.highlight.update(
            text=form.cleaned_data["text"],
            book=form.cleaned_data["book"],
            tags=form.cleaned_data["tags"],
        )
        messages.add_message(self.request, messages.INFO, f"Highlight updated!")
        return redirect("highlights:list")


def confirm_delete(request, pk):
    return render(request, "highlights/partials/confirm-delete.html", {"pk": pk})


@login_required
def delete(request, pk):
    highlight = get_object_or_404(models.Highlight, user=request.user, pk=pk)
    highlight.delete()
    return HttpResponse()
