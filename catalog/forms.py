from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.
from .models import BookInstance
from django import forms


class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'imprint', 'due_back', 'borrower', 'status']
        widgets = {
            'imprint': forms.DateInput(attrs={'type': 'date'}),
            'due_back': forms.DateInput(attrs={'type': 'date'}),
        }


class ReserveBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        widgets = {
          'due_back': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
          'due_back': 'Дата возврата'
        }

    def clean_due_back(self):
      data = self.cleaned_data['due_back']

      # Check if a date is not in the past.
      if data < datetime.date.today():
        raise ValidationError(_('Invalid date - renewal in past'))

      # Check if a date is in the allowed range (+4 weeks from today).
      if data > datetime.date.today() + datetime.timedelta(weeks=4):
        raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

      return data
