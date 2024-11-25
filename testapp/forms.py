from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from account.models import profile
from testapp.models import voyage,categorieVoyage,Reservation


class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email','password1','password2']
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']
class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model=User
        fields = ['old_password','new_password1','new_password2']

class updateprofileform(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['username', 'email', 'phone', 'adress']

    def save(self, commit=True):
        profile_instance = super().save(commit=False)

        # Get the associated User model
        user_instance = profile_instance.user

        # Update User model fields
        user_instance.username = self.cleaned_data['username']  # Replace 'username' with the actual field name
        user_instance.email = self.cleaned_data['email']  # Replace 'email' with the actual field name

        if commit:
            # Save both User and Profile models
            user_instance.save()
            profile_instance.save()

        return profile_instance
class VoyageForm(forms.ModelForm):
    class Meta:
        model = voyage
        fields = ['ville_origine', 'ville_destination', 'date_aller', 'date_retour', 'nombre_personnes', 'description', 'prix']
        widgets = {
            'date_aller': forms.DateInput(attrs={'type': 'date'}),
            'date_retour': forms.DateInput(attrs={'type': 'date'}),
        }
# class CategoryForm (forms.ModelForm):
#     class Meta:
#         model=categorieVoyage
#         fields=['titre_categ','description_courte','reduction_percent']
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'datetime', 'destination', 'special_request', 'number_of_persons', 'baggage_weight_kg']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


