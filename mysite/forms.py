from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MyRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	user_age = forms.IntegerField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'user_age','password1', 'password2')

	def save(self, commit=True):
		user = super(MyRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.user_age = self.cleaned_data['user_age']

		if commit:
			user.save()

		return user

class ProductFeatureForm(forms.Form):
	product_selection = forms.ChoiceField(required=False)
	feature_selection = forms.ChoiceField(required=False)

	