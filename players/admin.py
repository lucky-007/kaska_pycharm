from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from players.forms import PlayerChangeForm, PlayerCreationForm

from players.models import Player


class PlayerAdmin(UserAdmin):
    form = PlayerChangeForm
    add_form = PlayerCreationForm

    list_display = ('surname', 'name', 'phone', 'stud_photo', 'is_student', 'is_paid', 'is_admin', 'pool',)
    list_display_links = ('surname', 'name')

    list_editable = ('is_student', 'is_paid', 'pool',)
    list_filter = ('is_student', 'is_paid', 'is_admin', 'pool')

    search_fields = ('surname',)
    ordering = ('surname',)

    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Player data', {'fields': ('surname', 'name', 'sex', 'university', 'stud_photo', 'phone', 'experience', 'position',
                                    'fav_throw', 'style', 'size',)
                         }
         ),
        ('Hidden data', {'fields': ('vk_id', 'access_token', 'pool', 'is_active', 'is_admin', 'is_superuser',
                                    'is_student', 'is_paid', 'date_joined', 'photo',)
                         }
         ),
    ]

    add_fieldsets = [
        (None, {'fields': ('email', 'password1', 'password2', 'surname', 'name', 'university', 'stud_photo',
                           'experience', 'position', 'fav_throw', 'style', 'size',)
                }
         ),
    ]


admin.site.register(Player, PlayerAdmin)
admin.site.unregister(Group)
