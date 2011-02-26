from django.conf.urls.defaults import patterns, url
from django.views.generic.list_detail import object_detail
from models import InterestGroup

groups_dict = {
    'queryset': InterestGroup.objects.public(),
}

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w_-]+)/$', object_detail, groups_dict, name='group_detail'),
)
