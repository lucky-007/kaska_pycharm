from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

CHOICES_POSITION = (
    ('han', 'Handler'),
    ('mid', 'Middle'),
    ('lon', 'Long'),
    ('sid', 'On sideline')
)

CHOICES_STYLE = (
    ('slow', 'SlowPock'),
    ('regul', 'Regular'),
    ('cheek', 'cheeky'),
    ('uncon', 'Uncontrollable'),
    ('drunk', 'Drunk'),
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
            raise ValueError('Email address is required')

        now = timezone.now()

        user = self.model(
            email=self.normalize_email(email),
            surname=surname,
            name=name,
            university=university.upper(),
            experience=experience,
            vk_link=vk_link.lower(),
            position=position,
            fav_throw=fav_throw,
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
        # verbose_name='Email',
        max_length=255,
        unique=True,
        blank=False,
        error_messages={
            # 'unique': 'Этот email уже зарегистрирован'
            'unique': "We've have already this"
        }
    )
    surname = models.CharField(
        # verbose_name='Фамилия',
        max_length=25,
        blank=False,
    )
    name = models.CharField(
        # verbose_name='Имя',
        max_length=15,
        blank=False,
    )
    university = models.CharField(
        # verbose_name='Университет',
        max_length=15,
        blank=False,
    )
    experience = models.PositiveSmallIntegerField(
        # verbose_name='Опыт игры (лет)',
        blank=False,
    )
    vk_link = models.URLField(
        # verbose_name='Ссылка на vk-профиль',
        unique=True,
        blank=False,
        default='http://vk.com/',
        error_messages={
            # 'unique': 'Этот email уже зарегистрирован'
            'unique': "We've have already this"
        }
    )
    position = models.CharField(
        # verbose_name='Любимая позиция',
        max_length=3,
        choices=CHOICES_POSITION,
        blank=False,
    )
    fav_throw = models.CharField(
        # verbose_name='Любимый бросок',
        max_length=15,
        blank=False,
    )
    style = models.CharField(
        # verbose_name='Стиль игры',
        max_length=5,
        choices=CHOICES_STYLE,
        blank=False,
    )
    size = models.CharField(
        # verbose_name='Размер футболки',
        max_length=2,
        choices=CHOICES_SIZE,
        blank=False,
    )

    stud_photo = models.ImageField(
        # verbose_name='Фотография студенческого билета',
        help_text='Можно загрузить фотографию позже',
        blank=True,
    )

    # Hidden fields for users:
    pool = models.SmallIntegerField(default=0)
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

    @property
    def is_staff(self):
        return self.is_admin
