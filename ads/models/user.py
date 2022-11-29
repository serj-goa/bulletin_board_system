from django.db import models as m
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .location import Location

__all__ = ('User', )


class User(AbstractUser):
    ROLE = (
        ('member', _('Member')),
        ('moderator', _('Moderator')),
        ('admin', _('Administrator')),
    )
    role = m.CharField(verbose_name=_('Role'), max_length=16, choices=ROLE, blank=False, db_index=True)
    age = m.SmallIntegerField(verbose_name=_('Age'), null=False)
    location = m.ForeignKey(verbose_name=_('Address'), to=Location, related_name='users', on_delete=m.PROTECT, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def json_representation(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "age": self.age,
            "address": self.location.address if self.location else None,
        }

    def __str__(self):
        return self.first_name
