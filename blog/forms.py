from django import forms

from .models import *

class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

#use of modelsForm
class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content']

    def clean_slug(self, *args, **kwargs):
        instance = self.instance
        
        print(instance)
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("this title is already used...")
        return title