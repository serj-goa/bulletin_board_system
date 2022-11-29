from django.db import models as m
from django.utils.translation import gettext_lazy as _

from .category import Category
from .user import User

__all_ = ('Ad', )


class Ad(m.Model):
    name = m.CharField(verbose_name=_('Name'), max_length=64, blank=False, db_index=True)
    author = m.ForeignKey(verbose_name=_('Author'), to=User, related_name='ads', on_delete=m.CASCADE, null=False)
    price = m.DecimalField(verbose_name=_('Price'), max_digits=12, decimal_places=2, null=True)
    description = m.CharField(verbose_name=_('Description'), max_length=16*1024, blank=False)
    is_published = m.BooleanField(verbose_name=_('Is published'), default=False, db_index=True)
    image = m.ImageField(verbose_name=_('Image'), upload_to='ads', blank=True)
    category = m.ForeignKey(verbose_name=_('Category'), to=Category, related_name='ads', on_delete=m.PROTECT, null=False)

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')
        ordering = ('category__name', 'author', 'name')

    @property
    def json_representation(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author.json_representation,
            "price": self.price,
            "description": self.description,
            "is_published": self.is_published,
            "category": self.category.json_representation,
            "image": self.image.url if self.image else None
        }

    def __str__(self):
        return self.name
