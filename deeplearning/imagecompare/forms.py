from django import forms
from .models import Image, Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )