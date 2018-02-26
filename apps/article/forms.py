from django import forms


class AddArticleForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True)
    cover_img = forms.ImageField(required=True)
