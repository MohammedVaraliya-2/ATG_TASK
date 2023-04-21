from django.core.files.base import ContentFile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': False}))
    email = forms.EmailField(max_length=254, required=True)
    address_line1 = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_picture', 'address_line1', 'city', 'state', 'pincode')
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        user_profile = UserProfile(user=user)
        user_profile.address_line1 = self.cleaned_data['address_line1']
        user_profile.city = self.cleaned_data['city']
        user_profile.state = self.cleaned_data['state']
        user_profile.pincode = self.cleaned_data['pincode']
        if self.cleaned_data['profile_picture']:
            # Save the uploaded image file with the user's username as the filename
            image_file = self.cleaned_data['profile_picture']
            file_extension = image_file.name.split('.')[-1]
            file_name = f'{user.username}.{file_extension}'
            user_profile.profile_picture.save(file_name, ContentFile(image_file.read()), save=False)
        user_profile.save()
        return user
