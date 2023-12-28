from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.core.exceptions import ValidationError

# Create your forms here.

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label='Email add', widget=forms.EmailInput(attrs={'placeholder':'Email address'}))
	phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial=''),)
	first_name = forms.CharField(required=True, label='First name', widget=forms.TextInput(attrs={'placeholder' : 'Your name'}))
	last_name = forms.CharField(required=True, label='Last name', widget=forms.TextInput(attrs={'placeholder' : 'Your surname'}))
	other_name = forms.CharField(required=False, label='Other name', widget=forms.TextInput(attrs={'placeholder' : 'Other name'}))
	username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'placeholder' : 'Create username'}))
	password2 = forms.CharField(required=True, label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm password'}))
	required_css_class = 'required'
	password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'placeholder' : 'Set password'}))
	required_css_class = 'required'

	class Meta:
		model = User
		fields = ("first_name", "last_name", "other_name", "username", "phone_number", "email", "password1", "password2" )


	def clean_username(self):
		username = self.cleaned_data['username']
		check = User.objects.filter(username = username)
		if check.exists():
			raise ValidationError(f'Username {username} is already taken')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		check = User.objects.filter(email = email)
		if check.exists():
			raise ValidationError(f'Email {email} already exist')
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
	
		if password1 and password2 and password1 != password2:
			raise ValidationError("Password don't match")

	# def clean_phone_number(self):
	# 	phone_number = self.cleaned_data['phone_number']
	# 	check = User.objects.filter(phone_number = phone_number)
	# 	if check.exists():
	# 		raise ValidationError(f'Email {phone_number} already registered')
	# 	return phone_number

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.username = self.cleaned_data['username']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.password1 = self.cleaned_data['password1']
		if commit:
			user.save()
		return user
