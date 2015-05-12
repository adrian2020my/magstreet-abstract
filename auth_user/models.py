from django.db import models
from django.contrib.auth.backends import ModelBackend
# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.timezone import datetime
from django.forms import extras
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from auth_user.fields import JSONField

#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#   if created:
#        Token.objects.create(user=instance)



class MyUser(AbstractUser):
    gender = models.CharField(max_length=6)
    dob = models.DateField(null=True)
    is_authenticated = models.BooleanField(default=False)
    agree_toc = models.BooleanField(default=True)
#    facebook_token = models.CharField(max_length=100, default=' ')


class FbAccount(models.Model):
    user = models.OneToOneField(MyUser, related_name='user_id')
    access_token = models.TextField(verbose_name=_('Facebook User \'s Access Token'))
    uid = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    extra_data = JSONField(verbose_name=_('extra data'), default='{}')
    expires_at = models.DateTimeField(blank=True, null=True,
                                      verbose_name=_('expires at'))


class RegisterForm(UserCreationForm):

    dob = forms.DateField(label='Date of Birth', required=False,
                          widget=extras.SelectDateWidget(years=[y for y in range(1900, datetime.now().year + 1)])
                          )
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username_validator = RegexValidator(regex='^[a-z0-9_-]{3,16}$',
                                        message='No Special Symbols allowed. Alphanumerics only',
                                        code='invalid',
                                        )
    gender = forms.ChoiceField(label='Gender', choices=SEX, widget=forms.Select(attrs={'class': 'regDropDown'}))
    # agree_toc = forms.BooleanField(label='', help_text='Do you agree with our Terms and Conditions?', initial=True, required=False)
    username = forms.CharField(label="Username", widget=forms.TextInput(), max_length=15, help_text='Required. less than 30 characters. Alphanumerics only.', validators=[username_validator])
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="Email Address", widget=forms.TextInput(), required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'dob', 'gender')

    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(_('Username "%s" is already in use.' % username), code='invalid')
        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('Email address "%s" is already in use.' % email), code='invalid')
        return email

    def save(self):
        new_user = MyUser.objects.create_user(self.cleaned_data['username'],
                                          self.cleaned_data['email'],
                                          self.cleaned_data['password2'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.dob = self.cleaned_data['dob']
        new_user.gender = self.cleaned_data['gender']
        new_user.save()


