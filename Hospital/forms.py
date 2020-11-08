from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  # UserCreationForm  import garnu ko karan vaneko yesle djagno le
                                                        # User ko lagi diyeko authentication form automatic dinxa... yo form use garyo vani password lai 
                                                        # manually hash garnu pardaina... django le automatic hash gardinxa  & Username pahilai nai use vako
                                                        # xa ki nai vanera check garne code lekhnu parena ... django le automatic check gardinxa
from django.contrib.auth.models import User  # yaha User vaneko django le diyeko inbuilt User model ho
from django import forms  # forms.py page ma yo forms vanni import garnai parxa
from django.db import transaction
from .models import *
from django.core.exceptions import ValidationError


class CreateClientForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {"username": None,
                      "email": None,
                      "password2": None
                      }

    # For making username & email address to be unique so that while resetting password it doesn't get conflict with other user.
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("User having this email already exists.")
        return self.cleaned_data

    @transaction.atomic  # However, if an exception happens in a function decorated with transaction.atomic, then you don't have anything 
                         #to do, it'll rollback automatically to the savepoint created by the decorator before running the your function, as documented.
                         # transaction.atomic  allows us to create a block of code within which the atomicity on the database is guaranteed. 
                         #If the block of code is successfully completed, the changes are committed to the database. If there is an exception, 
                         #the changes are rolled back.
    def save(self):
        user = super().save(
            commit=False)  # yesle form bata database ma value store garni bela ma, user le form ma navareko filed 
                           #i.e(is_student & is_teacher) both field lai False garauxa i.e( 0 garauxa).
        user.is_client = True  # aba chai table ko is_student vanni field lai balla aba Ture garauxa i.e (1 garauxa)
        user.is_admin = False
        user.save()  # again, save to database
        # Client.objects.create(user=user)      # Student model ko student vanni object create gareko
        return user


