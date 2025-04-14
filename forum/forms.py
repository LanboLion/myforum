from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': '支持@提及功能'}),
        }