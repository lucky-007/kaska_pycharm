from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from players.models import Player


CHOICES_FILTER = (
    ('sur', _('Surname')),
    ('univer', pgettext_lazy('Search by', 'University')),
    ('paid', _('Have already paid')),
    ('stud', _('Have valid student ID')),
    ('play', _('Registered as players'))
)


class SearchForm(forms.Form):
    s = forms.CharField(label='', max_length=50, required=False,
                        widget=forms.TextInput(attrs={'placeholder': _('Search')}))
    o = forms.ChoiceField(label=_('Sorted by:'), choices=CHOICES_FILTER, initial='sur')


class PlayerCreationForm(forms.ModelForm):
    """
    A form for creating new users with doubled password
    """
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password')}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password confirmation')}))
    phone = forms.CharField(validators=[RegexValidator(regex='^[+]{0,1}[0-9]{10,12}$',
                                                       message=_('Use only "+" and numbers'),
                                                       code='invalid_phone')
                                        ],
                            widget=forms.TextInput(attrs={'placeholder': _('Phone')}))

    class Meta:
        model = Player
        fields = ('email', 'password1', 'password2', 'surname', 'name', 'university', 'stud_photo', 'experience',
                  'position', 'fav_throw', 'style', 'size', 'phone',)
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': _('Email')}),
            'surname': forms.TextInput(attrs={'placeholder': _('Last name')}),
            'name': forms.TextInput(attrs={'placeholder': _('First name')}),
            'university': forms.TextInput(attrs={'placeholder': pgettext_lazy('Model', 'University')}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super(PlayerCreationForm, self).save(commit=False)
        user.make_nice()
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class PlayerChangeForm(forms.ModelForm):
    """
    A form for changing user profile
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Player
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']

    def save(self, commit=True):
        user = super(PlayerChangeForm, self).save(commit=False)
        user.make_nice()
        if commit:
            user.save()
        return user


class PlayerSelfChangeForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('stud_photo',)

    def save(self, commit=True):
        user = super(PlayerSelfChangeForm, self).save(commit=False)
        user.make_nice()
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Authentication players
    """
    email = forms.EmailField(max_length=255)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _('Incorrect combination of %(username)s and password'),
        'inactive': _('This account is inactive'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
