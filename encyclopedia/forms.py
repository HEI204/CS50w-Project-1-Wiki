from django import forms
from . import util


class AddNewEntryForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control col-lg-6 col-md-6'}),
        max_length=100,
        required=True
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control col-lg-6 col-md-6'}),
        required=True
    )

    def clean_title(self):
        new_entry_title = self.cleaned_data["title"]

        if not util.get_entry(new_entry_title) is None:
            self.fields["title"].widget.attrs["class"] += " is-invalid"
            raise forms.ValidationError(
                "This title is already exist, please try another title!")
        return new_entry_title


class EditEntryForm(forms.Form):
    content = forms.CharField(
        label="Edit entry's content (use Markdown language)",
        widget=forms.Textarea(
            attrs={'class': 'form-control col-lg-6 col-md-6'}),
        required=True
    )
