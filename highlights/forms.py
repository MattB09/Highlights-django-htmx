from django import forms


class Highlight(forms.Form):
    text = forms.CharField(max_length=None, required=True, widget=forms.Textarea)
    book = forms.ModelChoiceField(queryset=None, required=True)
    tags = forms.ModelMultipleChoiceField(
        queryset=None, required=False, widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        tags = kwargs.pop("tags")
        books = kwargs.pop("books")
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = books
        self.fields["tags"].queryset = tags
