from django import forms
from .models import Page,Division,Story,Picture
class PageForm(forms.ModelForm):
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        #exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        fields = ('name','des','division')



class storyForm(forms.ModelForm):
    class Meta:
        model=Story
        fields = ('story_page','title_name','member','des')
        help_texts = {
            'story_page': 'Select a Page',
            'title_name': 'Give a title',
            'memeber': 'how many member ?',
            'des': 'How was your travel ?',
        }
class imageForm(forms.ModelForm):
    class Meta:
        model=Picture
        fields=('file',)
        help_texts={'file':'Upload an image '}