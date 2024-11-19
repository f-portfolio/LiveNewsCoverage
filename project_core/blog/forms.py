from django.contrib import admin
from django import forms
from .models import Post

class MyModelAdminForm(forms.ModelForm):
    word_count = forms.IntegerField(label='Word Count', required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.content:
            word_count = len(instance.content.split())
            self.fields['word_count'].initial = word_count
            self.fields['word_count'].widget.attrs['readonly'] = True
