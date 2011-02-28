from django.views.generic.simple import direct_to_template
from models import InterestGroup
from taggit.models import Tag

def index(request, template_name='groups/index.html', extra_context=None):
    """Main view for the site"""

    ctx = {
        'public_groups'  : InterestGroup.objects.public(),
        'private_groups' : InterestGroup.objects.private(),
        'tags'           : Tag.objects.all(),
    }

    if extra_context:
        ctx.update(extra_context)
    return direct_to_template(request, template_name, extra_context=ctx)
