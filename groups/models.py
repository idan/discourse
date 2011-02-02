from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class InterestGroup(models.Model):
    """The group holding the events"""

    name        = models.CharField(_('Name'), max_length=70, unique=True)
    public      = models.BooleanField(_('Public'), default=True)
    slug        = models.SlugField(_('Slug'), max_length=70, blank=True,
                    unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    members     = models.ManyToManyField(User, related_name='interest_groups',
                    through='Membership', verbose_name=_('Members'))

    class Meta:
        verbose_name = _('Interest group')
        verbose_name_plural = _('Interest groups')


MEMBERSHIP_LEVELS = (
    (0, _('Limited')),
    (1, _('Full')),
    (2, _('Group admin')),
)

class Membership(models.Model):
    """Group membership, used as `thorugh` model
    for InterestGroup and a User

    """
    user   = models.ForeignKey(User, verbose_name=_('User'))
    group  = models.ForeignKey(InterestGroup, verbose_name=_('Interest group'))
    joined = models.DateField(_('Date joined'), auto_now_add=True)
    level  = models.IntegerField(_('Membership level'), choices=MEMBERSHIP_LEVELS)

    class Meta:
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')
