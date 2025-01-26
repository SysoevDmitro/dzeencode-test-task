from io import BytesIO

from PIL import Image
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Comment
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    """ Form for creating comment"""
    captcha_field = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'text', 'file', 'captcha_field']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 102400:  # 100 KB
                raise forms.ValidationError("File size exceeds 100KB.")

            if file.name.endswith('.txt'):
                return file
            elif file.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                try:
                    img = Image.open(file)
                    if img.width > 320 or img.height > 240:
                        img.thumbnail((320, 240))
                        buffer = BytesIO()
                        img.save(buffer, format=img.format)
                        buffer.seek(0)
                        return InMemoryUploadedFile(
                            buffer, None, file.name, file.content_type, buffer.tell(), None
                        )
                except Exception:
                    raise forms.ValidationError("Invalid image file.")
            else:
                raise forms.ValidationError("Invalid file type. Allowed: .txt, .jpg, .jpeg, .png, .gif.")
        return file
