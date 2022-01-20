from django import forms
from .models import Article


class ArticleCreateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Article
        fields = ['title', 'short_description', 'description', 'image']
        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
