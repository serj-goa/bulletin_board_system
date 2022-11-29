from django.db import models as m
from django.utils.translation import gettext_lazy as _

__all__ = ('Location', )


class Location(m.Model):
    address = m.CharField(verbose_name=_('Address'), max_length=300, blank=False)
    latitude = m.DecimalField(verbose_name=_('Latitude'), max_digits=8, decimal_places=6, null=False)
    longitude = m.DecimalField(verbose_name=_('Longitude'), max_digits=8, decimal_places=6, null=False)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.address
