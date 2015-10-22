from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from players.models import Player


class PlayerCreationForm(forms.ModelForm):
    """
    A form for creating new users with doubled password
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Player
        fields = ('email', 'password1', 'password2', 'surname', 'name', 'university', 'stud_photo', 'experience',
                  'vk_link', 'position', 'fav_throw', 'style', 'size',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(PlayerCreationForm, self).save(commit=False)
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


class PlayerAdmin(UserAdmin):
    # TODO try initial to add_form/vk_link
    form = PlayerChangeForm
    add_form = PlayerCreationForm

    list_display = ('surname', 'name', 'vk_link', 'stud_photo', 'is_student', 'is_paid', 'is_admin', 'pool',)
    list_display_links = ('surname', 'name')

    list_editable = ('is_student', 'is_paid', 'pool',)
    list_filter = ('is_admin', 'is_paid', 'pool')

    search_fields = ('surname',)
    ordering = ('surname',)

    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Player data', {'fields': ('surname', 'name', 'university', 'stud_photo', 'experience', 'vk_link', 'position',
                                    'fav_throw', 'style', 'size',)
                         }
         ),
        ('Hidden data', {'fields': ('pool', 'is_active', 'is_admin', 'is_superuser', 'is_student', 'is_paid',
                                    'date_joined', 'photo',)
                         }
         ),
    ]

    add_fieldsets = [
        (None, {'fields': ('email', 'password1', 'password2', 'surname', 'name', 'university', 'stud_photo',
                           'experience', 'vk_link', 'position', 'fav_throw', 'style', 'size',)
                }
         ),
    ]


admin.site.register(Player, PlayerAdmin)
admin.site.unregister(Group)
