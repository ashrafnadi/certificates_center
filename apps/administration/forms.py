from django import forms

from .models import faculty


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=60,
        label='اسم المستخدم',
        widget=forms.TextInput(attrs={
            'placeholder': 'أدخل اسم المستخدم',
            'class': 'input input-bordered w-full'
        })
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'أدخل كلمة المرور',
            'class': 'input input-bordered w-full'
        })
    )
    faculty = forms.ModelChoiceField(
        queryset=faculty.objects.none(),
        label='الكلية',
        required=False,
        empty_label='-- اختر الكلية --',
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = faculty.objects.all().order_by('faculty_ar_name')