from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.text import capfirst
UserModel = User()

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        # self.helper.form_class = 'blueForms'
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'submit_survey'
        # self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
    
    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.active = False
        # obj.set_password(self.cleaned_data.get('username'))
        if commit:
            obj.save()
        return obj
    

class LoginForm(AuthenticationForm):    
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)
        # Form Helper Start from here.
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update'))