from django.db import IntegrityError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField


class Channel(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    slug = AutoSlugField(
        verbose_name=_('Slug'), populate_from='name', max_length=260)

    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            raise IntegrityError('Name is required.')

        return super(Channel, self).save(*args, **kwargs)
