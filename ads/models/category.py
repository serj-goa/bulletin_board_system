from django.db import models as m
from django.utils.translation import gettext_lazy as _

__all__ = ('Category', )


class Category(m.Model):
    name = m.CharField(verbose_name=_('Name'), max_length=64, blank=False, db_index=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name', )

    @property
    def json_representation(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

    def __str__(self):
        return self.name
