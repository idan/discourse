from django.db import models
from django.utils.translation import ugettext_lazy as _

class InterestGroup(models.Model):
    """The group holding the events"""

    name        = models.CharField(_('Name'), max_length=70, unique=True)
    public      = models.BooleanField(_('Public'), default=True)
    slug        = models.SlugField(_('Slug'), max_length=70, blank=True,
                    unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Interest group')
        verbose_name_plural = _('Interest groups')
