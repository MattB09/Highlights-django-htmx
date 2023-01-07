from django.contrib.auth import mixins
from django.contrib import messages
from django.views import generic
from django.shortcuts import redirect, render, HttpResponse

from highlights import forms
from highlights import models


class Add(mixins.LoginRequiredMixin, generic.FormView):
    template_name = "highlights/tags/add.html"
    form_class = forms.Tag
    
    def get_template_names(self):
        if self.request.htmx:
            return ["highlights/partials/tags/form.html"]
        return ["highlights/tags/add.html"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            context["hx_tag"] = True
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        models.Tag.new(
            tag=form.cleaned_data["tag"], 
            user=self.request.user,
        )
        messages.add_message(self.request, messages.INFO, "Tag added!")
        
        if self.request.htmx:
            return HttpResponse("Success motha fuckaa!")
        return redirect("highlights:list")
    
class HxRefreshTags(mixins.LoginRequiredMixin, generic.ListView):
    template_name = "highlights/partials/list.html"
    model = models.Tag
    context_object_name = "tags"
    