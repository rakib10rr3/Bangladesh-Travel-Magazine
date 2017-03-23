from django import forms
from django.forms import Textarea, TextInput, NumberInput, FileInput

from .models import Page, Story, Picture, Comment, UserProfile


class PageForm(forms.ModelForm):
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        # exclude = ('category',)
        # or specify the fields to include (i.e. not include the category field)
        fields = ('name', 'des')
        help_texts = {
            'name': 'Place Name',
            'des': 'One line description for the place',
        }
        # Widgets Name: https://docs.djangoproject.com/en/dev/ref/forms/widgets/
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'des': Textarea(attrs={'class': 'form-control'}),
        }


class storyForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title_name', 'member','budget','type_name', 'des')
        help_texts = {
            'title_name': 'Give an Awesome title of the Tour!',
            'member': 'How many member traveled with you?',
            'budget': 'What was Your budget ?',
            'type_name': 'Please Select a Type',
            'des': 'How was your travel?',
        }
        widgets = {
            'title_name': TextInput(attrs={'class': 'form-control'}),
            'member': NumberInput(attrs={'class': 'form-control'}),
            'budget': TextInput(attrs={'class': 'form-control'}),
            'des': Textarea(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'birth_date', 'gender', 'country')


class imageForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('file',)
        help_texts = {'file': 'Upload an image'}
        widgets = {
            'file': FileInput(attrs={'class': 'btn btn-default'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
