from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

CHOICES_EXPERIENCE = (
    ('0-1', _('less than 1 year')),
    ('1-2', _('1-2 years')),
    ('2-3', _('2-3 years')),
    ('3-5', _('3-5 years')),
    ('>5', _('more than 5 years')),
)

CHOICES_POSITION = (
    ('han', _('Handler')),
    ('mid', _('Middle')),
    ('lon', _('Long')),
    ('sid', _('On sideline')),
)

CHOICES_THROW = (
    ('for', _('Forehand')),
    ('bac', _('Backhand')),
    ('bla', _('Blade')),
    ('ham', _('Hammer')),
    ('sco', _('Scoober')),
    ('ove', _('Overhand')),
    ('pus', _('Push-pass')),
)

CHOICES_STYLE = (
    ('uncon', _('Uncontrollable')),
    ('slow', _('SlowPock')),
    ('cheek', _('Cheeky')),
    ('drunk', _('Drunk')),
    ('banan', _('Banana-cut')),
)

CHOICES_SIZE = (
    ('xs', 'XS'),
    ('s', 'S'),
    ('m', 'M'),
    ('l', 'L'),
    ('xl', 'XL'),
)

CHOICES_SEX = (
    ('m', _('Male')),
    ('f', _('Female')),
)


class PlayerManager(BaseUserManager):
    def _create_user(self, email, surname, name, sex, university, experience, position, fav_throw, style, size, phone,
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
            sex=sex,
            name=name.capitalize(),
            university=university.upper(),
            experience=experience,
            position=position,
            fav_throw=fav_throw,
            style=style,
            size=size,
            phone=phone,

            date_joined=now,
            is_admin=is_admin,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, surname, name, sex, university, experience, position, fav_throw, style, size, phone,
                    password=None, **extra_fields):
        return self._create_user(email, surname, name, sex, university, experience, position, fav_throw, style,
                                 size, phone, password, False, False, **extra_fields)

    def create_superuser(self, email, password, surname, name, sex, university, experience, position, fav_throw,
                         style, size, phone, **extra_fields):
        return self._create_user(email, surname, name, sex, university, experience, position, fav_throw, style,
                                 size, phone, password, True, True, **extra_fields)


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
    sex = models.CharField(
        verbose_name=_('Sex'),
        max_length=1,
        choices=CHOICES_SEX,
        default='m',
        blank=False,
    )
    university = models.CharField(
        verbose_name=pgettext_lazy('Model', 'University'),
        max_length=50,
        blank=False,
    )
    phone = models.CharField(
        verbose_name=_('Phone'),
        max_length=13,
        blank=False,
        null=True,
    )

    # Choices
    experience = models.CharField(
        verbose_name=_('Experience'),
        max_length=3,
        choices=CHOICES_EXPERIENCE,
        default='0-1',
        blank=False,
    )
    position = models.CharField(
        verbose_name=_('Favourite position'),
        max_length=3,
        choices=CHOICES_POSITION,
        default='han',
        blank=False,
    )
    fav_throw = models.CharField(
        verbose_name=_('Favourite throw'),
        max_length=3,
        choices=CHOICES_THROW,
        default='for',
        blank=False,
    )
    style = models.CharField(
        verbose_name=_('Play style'),
        max_length=5,
        choices=CHOICES_STYLE,
        default='uncon',
        blank=False,
    )
    size = models.CharField(
        verbose_name=_('T-shirt size'),
        max_length=2,
        choices=CHOICES_SIZE,
        default='xs',
        blank=False,
    )

    stud_photo = models.ImageField(
        verbose_name=_('Student ID (photo)'),
        help_text=_('You can load the photo of the student ID later. For admins only'),
        blank=True,
    )

    # Hidden fields for users:
    vk_id = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=True,
    )
    access_token = models.CharField(
        null=True,
        max_length=100,
        blank=False,
    )
    pool = models.SmallIntegerField(default=0)
    photo = models.URLField(
        null=True,
        default='',
        blank=True,
    )
    team = models.ForeignKey('Team', null=True, blank=True)

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
        'sex',
        'university',
        'experience',
        'position',
        'fav_throw',
        'style',
        'size',
        'phone',
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
        self.university = self.university.upper()
        return None

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        ordering = ['surname']


class Team(models.Model):
    team_name = models.CharField(
        verbose_name=_('Team name'),
        max_length=50,
    )
    chosen = models.CharField(
        max_length=8,
        default=8*'0'
    )

    intimation1 = models.CharField(max_length=200)
    intimation2 = models.CharField(max_length=200)
    intimation3 = models.CharField(max_length=200)
    intimation4 = models.CharField(max_length=200)
    intimation5 = models.CharField(max_length=200)
    intimation6 = models.CharField(max_length=200)
    intimation7 = models.CharField(max_length=200)
    intimation8 = models.CharField(max_length=200)

    def get_intimation(self, pool):
        single_int = self._meta.get_field_by_name('intimation'+str(pool))[0]
        return single_int.value_to_string(self)

    def is_available(self, pool):
        if self.chosen[pool-1] == '0':
            return True
        else:
            return False

    def __str__(self):
        return self.team_name

    def __unicode__(self):
        return self.team_name
