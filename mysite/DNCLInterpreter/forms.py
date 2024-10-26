from django import forms
from .models import Code

class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={
                'placeholder': 'ここにDNCLコードを入力してください...',
                'rows': 15,
                'cols': 80,
                'style': 'width: 100%;'
            }),
        }