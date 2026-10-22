from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Book, Notes

class SiginForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        
        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            if Use.objects.filter(email__iexact=eamil).exits():
                raise forms.validationError("An account with this email exits")
            return email

class BookForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Book
        fields = ['title', 'author', 'summary', 'isbn', 'genre']
    
    # def clean(self):
    #     cleaned = super.clean()
    #     return cleaned

class NoteForm(forms.Form):
    title = forms.CharField(max_length=200, label="Note Title")
    body = forms.CharField(widget=forms.Textarea, label="Content")