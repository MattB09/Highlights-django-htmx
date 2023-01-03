from django import forms
from django.forms import ValidationError


from . import models


class Highlight(forms.Form):
    error_css_class = "text-red-600 text-sm"
    required_css_class = "::after'*'"
    
    book = forms.ModelChoiceField(queryset=None, required=True)
    text = forms.CharField(max_length=None, required=True, widget=forms.Textarea)
    tags = forms.ModelMultipleChoiceField(
        queryset=None, required=False, widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        tags = kwargs.pop("tags")
        books = kwargs.pop("books")
        try:
            self.highlight_id = kwargs.pop("highlight_id")
        except KeyError:
            self.highlight_id = None      
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = books
        self.fields["tags"].queryset = tags
        
    def clean_text(self):
        qs = models.Highlight.objects.find_duplicates(self.data["text"], self.highlight_id)
        if qs.exists():
            raise ValidationError("A Highlight with this text exists already")
        return self.data["text"]
