from django.db import IntegrityError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    slug = AutoSlugField(
        verbose_name=_('Slug'), populate_from='name', max_length=260,
        unique=True)

    # relations
    channel = models.ForeignKey(
        verbose_name=_('Channel'),
        to='channel.Channel', related_name='categories')
    parent = models.ForeignKey(
        verbose_name=_('Parent category'),
        to='category.Category', related_name='subcategories',
        null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            raise IntegrityError('Name is required.')

        if not self.channel_id:
            raise IntegrityError('Channel is required.')

        return super(Category, self).save(*args, **kwargs)
