from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Question



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email','college','name',)
    def clean(self):
        if 'sign_up' in self.data:
            cleaned_data = super(SignUpForm, self).clean()
            name = cleaned_data.get('name')
            email = cleaned_data.get('email')
            username = cleaned_data.get('username')
            college = cleaned_data.get('college')
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
#            if not name and not username and not email and not college and not password1:
#                raise forms.ValidationError('You have to write something and passwords should match!')


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email','college','name',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        #fields = ('username', 'email','college','score','name',)
        fields = UserChangeForm.Meta.fields


class ReplyForm(forms.ModelForm):
	class Meta:
		model=Question
		fields=('answer',)
