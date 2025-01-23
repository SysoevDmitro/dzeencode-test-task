from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'email', 'text', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 102400:  # 100 KB
                raise forms.ValidationError("File size exceeds 100KB for files.")
        return file
