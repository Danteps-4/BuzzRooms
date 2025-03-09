from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Room, Profile, Topic

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["name", "topic", "description"]

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ["username", "email"]

class ProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile
