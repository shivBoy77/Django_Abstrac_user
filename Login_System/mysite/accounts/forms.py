from . models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login
# from .signals import Profile

# User = get_user_model()


class RegisterationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=225, help_text="Required. valid email.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = User.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(
                    "Invalid email or password")


# class LoginForm(forms.Form):
#     email = forms.EmailField(label='Email')
#     password = forms.CharField(widget=forms.PasswordInput)

#     def __init__(self, request=None, *args, **kwargs):
#         self.request = request
#         super(LoginForm, self).__init__(*args, **kwargs)

#     def clean(self, request=None):
#         # request = self.request
#         data = self.cleaned_data
#         email = data.get("email")
#         password = data.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user is None:
#             raise forms.ValidationError("Invalid credentials")
#         login(self.request, user)
#         self.user = user
#         return data


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('full_name', 'email')


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('bio', 'location', 'birth_date')
