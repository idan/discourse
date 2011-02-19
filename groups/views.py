from django.views.generic.simple import direct_to_template

def index(request, template_name='groups/index.html', extra_context=None):
    """Main view for the site"""

    ctx = {
    }

    if extra_context:
        ctx.update(extra_context)
    return direct_to_template(request, template_name, extra_context=ctx)
