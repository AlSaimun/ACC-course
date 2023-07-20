from django.db import models
from django.contrib.auth.forms import SetPasswordForm
# Create your models here.
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password2'].label = 'Confirm Password'