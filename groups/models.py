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


class Event(models.Model):
    """An event by an InterestGroup"""

    group        = models.ForeignKey(InterestGroup, related_name='events',
                     verbose_name=_('Interest group'))
    start        = models.DateTimeField(_('Event start date and time'))
    end          = models.DateTimeField(_('Event end'), blank=True, null=True)
    description  = models.TextField(_('Description'), blank=True, null=True)
    slug         = models.SlugField(_('Slug'), max_length=50, unique=True,
                     help_text=_("Joined with group's slug forming the event's email address"))
    published    = models.BooleanField(_('Published'), default=False)
    location     = models.TextField(_('Location'), blank=True, null=True)
    registration = models.BooleanField(_('Registration required'), default=False)
    price        = models.DecimalField(_('Price'), max_digits=10,
                    decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __unicode__(self):
        """Show as event_slug.group_slug, e.g: ev17.pywebil"""

        return u'%(slug)s.%(group_slug)s' % {'group_slug':self.group.slug,
                'slug': self.slug }

class Talk(models.Model):
    """Talks for an event"""

    event   = models.ForeignKey(Event, verbose_name=_('Event'), related_name='talks')
    title   = models.CharField(_('Talk title'), max_length=100)
    content = models.TextField(_('Content'), blank=True, null=True)
    start   = models.TimeField(_('Start time'), blank=True, null=True)
    end     = models.TimeField(_('End time'), blank=True, null=True)

    class Meta:
        verbose_name = _('Talk')
        verbose_name_plural = _('Talks')
