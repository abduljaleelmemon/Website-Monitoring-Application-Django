from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.Charfield()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact = username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        return username