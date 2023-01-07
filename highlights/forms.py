from django import forms

from . import models

ERROR_CSS_CLASS = "text-red-800"
REQUIRED_CSS_CLASS = "::after'*'"
BORDER_CSS_CLASS = "border-2 border-indigo-300 rounded"


ERROR_CSS_CLASS = "text-red-800"
REQUIRED_CSS_CLASS = "::after'*'"
BORDER_CSS_CLASS = "border-2 border-indigo-300 rounded"


class Highlight(forms.Form):
    error_css_class = ERROR_CSS_CLASS
    required_css_class = REQUIRED_CSS_CLASS
    
    book = forms.ModelChoiceField(queryset=None, required=True, widget=forms.Select(attrs={"class": BORDER_CSS_CLASS}))
    text = forms.CharField(
        max_length=None, 
        required=True, 
        widget=forms.Textarea(attrs={"rows": 5, "class": BORDER_CSS_CLASS, "placeholder": "Highlight text...",}),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=None, required=False, widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        tags = kwargs.pop("tags")
        books = kwargs.pop("books")
        self.user = kwargs.pop("user")
        try:
            self.highlight_id = kwargs.pop("highlight_id")
        except KeyError:
            self.highlight_id = None      
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = books
        self.fields["tags"].queryset = tags
        
    def clean_text(self):
        qs = models.Highlight.objects.find_duplicates(self.user, self.data["text"], self.highlight_id)
        if qs.exists():
            raise forms.ValidationError("A Highlight with this text exists already")
        return self.data["text"]


class Tag(forms.Form):
    error_css_class = ERROR_CSS_CLASS
    required_css_class = REQUIRED_CSS_CLASS
    
    tag = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={"class": BORDER_CSS_CLASS}), 
        error_messages={"unique": "This tag already exists!"}
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        try:
            self.tag_id = kwargs.pop("tag_id")
        except KeyError:
            self.tag_id = None  
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        qs = models.Tag.objects.filter(user=self.user, tag=cleaned_data["tag"]).exclude(id=self.tag_id)
        print("QSSS", qs)
        if qs.exists():
            raise forms.ValidationError("This tag already exists.", code="duplicate")
