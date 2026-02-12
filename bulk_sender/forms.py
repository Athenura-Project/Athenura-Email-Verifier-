from django import forms

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    file = forms.FileField(
        help_text="CSV with email column",
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed")
        return file
