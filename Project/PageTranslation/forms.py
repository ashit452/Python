
from pydoc import pager
from django import forms
from PageTranslation.models import pageTranslation

class PageTranslationForm(forms.ModelForm):
    class Meta():
        model = pageTranslation
        fields = ('page','language','title','content')
        widgets = {'language': forms.HiddenInput()}

        # widgets = {
        #     'title': forms.TextInput(attrs={'class':'textinputclass'}),
        #     'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        # }