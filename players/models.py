from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

CHOICES_POSITION = (
    ('han', _('Handler')),
    ('mid', _('Middle')),
    ('lon', _('Long')),
    ('sid', _('On sideline')),
)

CHOICES_STYLE = (
    ('slow', _('SlowPock')),
    ('regul', _('Regular')),
    ('cheek', _('Cheeky')),
    ('uncon', _('Uncontrollable')),
    ('drunk', _('Drunk')),
)

CHOICES_SIZE = (
    ('xs', 'XS'),
    ('s', 'S'),
    ('m', 'M'),
    ('l', 'L'),
    ('xl', 'XL'),
)


class PlayerManager(BaseUserManager):
    def _create_user(self, email, surname, name, university, experience, vk_link, position, fav_throw, style, size,
                     password, is_admin, is_superuser, **extra_fields):
        """
        Creates and saves user by all required params.
        """
        if not email:
            raise ValueError(_('Email address is required'))

        now = timezone.now()

        user = self.model(
            email=self.normalize_email(email),
            surname=surname.capitalize(),
            name=name.capitalize(),
            university=university.upper(),
            experience=experience,
            vk_link=vk_link.lower(),
            position=position,
            fav_throw=fav_throw.capitalize(),
            style=style,
            size=size,

            date_joined=now,
            is_admin=is_admin,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, surname, name, university, experience, vk_link, position, fav_throw, style, size,
                    password=None, **extra_fields):
        return self._create_user(email, surname, name, university, experience, vk_link, position, fav_throw, style,
                                 size, password, False, False, **extra_fields)

    def create_superuser(self, email, password, surname, name, university, experience, vk_link, position, fav_throw,
                         style, size, **extra_fields):
        return self._create_user(email, surname, name, university, experience, vk_link, position, fav_throw, style,
                                 size, password, True, True, **extra_fields)


class Player(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=255,
        unique=True,
        blank=False,
        error_messages={
            'unique': _("We've have already this email")
        }
    )
    surname = models.CharField(
        verbose_name=_('Last name'),
        max_length=25,
        blank=False,
    )
    name = models.CharField(
        verbose_name=_('First name'),
        max_length=15,
        blank=False,
    )
    university = models.CharField(
        verbose_name=pgettext_lazy('Model', 'University'),
        max_length=15,
        blank=False,
    )
    experience = models.PositiveSmallIntegerField(
        verbose_name=_('Experience'),
        blank=False,
        default=0,
    )
    vk_link = models.URLField(  # TODO unavailable to change by player
        verbose_name=_('Link to vk profile'),
        unique=True,
        blank=False,
        default='http://vk.com/',
        error_messages={
            'unique': _("We've have already this")
        }
    )
    position = models.CharField(
        verbose_name=_('Favourite position'),
        max_length=3,
        choices=CHOICES_POSITION,
        blank=False,
    )
    fav_throw = models.CharField(
        verbose_name=_('Favourite throw'),
        max_length=15,
        blank=False,
    )
    style = models.CharField(
        verbose_name=_('Play style'),
        max_length=5,
        choices=CHOICES_STYLE,
        blank=False,
    )
    size = models.CharField(
        verbose_name=_('T-shirt size'),
        max_length=2,
        choices=CHOICES_SIZE,
        blank=False,
    )

    stud_photo = models.ImageField(
        verbose_name=_('Student ID (photo)'),
        help_text=_('You can load the photo of the student ID later. For admins only'),
        blank=True,
    )

    # Hidden fields for users:
    pool = models.SmallIntegerField(default=0)
    photo = models.URLField(
        null=True,
        default='',
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = PlayerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'surname',
        'name',
        'university',
        'experience',
        'vk_link',
        'position',
        'fav_throw',
        'style',
        'size',
    ]

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        full_name = '%s %s' % (self.surname, self.name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()

    def make_nice(self):
        self.surname = self.surname.capitalize()
        self.name = self.name.capitalize()
        self.fav_throw = self.fav_throw.capitalize()
        self.university = self.university.upper()
        self.vk_link = self.vk_link.lower()
        return None

    @property
    def is_staff(self):
        return self.is_admin
