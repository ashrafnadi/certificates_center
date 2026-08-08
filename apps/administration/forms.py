from django import forms

from .models import Faculty


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=60,
        label="اسم المستخدم",
        widget=forms.TextInput(
            attrs={
                "placeholder": "أدخل اسم المستخدم",
                "class": "input input-bordered w-full",
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "أدخل كلمة المرور",
                "class": "input input-bordered w-full",
                "autocomplete": "current-password",
            }
        ),
    )
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.none(),
        label="الكلية",
        required=False,
        empty_label="-- اختر الكلية --",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    def __init__(self, *args, allowed_faculties=None, **kwargs):
        super().__init__(*args, **kwargs)
        if allowed_faculties is not None:
            self.fields["faculty"].queryset = allowed_faculties
        else:
            self.fields["faculty"].queryset = Faculty.objects.all().order_by(
                "faculty_ar_name"
            )
