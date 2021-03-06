from django.contrib import admin
from models import InterestGroup, Membership, Event, Talk
from attachments.admin import AttachmentInlines

class MembershipsInline(admin.TabularInline):
    model = Membership

class InterestGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = (MembershipsInline, )

class TalksInline(admin.StackedInline):
    model = Talk


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (TalksInline, )
    list_display = ('title', 'group', 'start', 'end', 'published')
    list_filter = ('group', 'published')
    inlines = (TalksInline,
               AttachmentInlines,
              )

admin.site.register(InterestGroup, InterestGroupAdmin)
admin.site.register(Event, EventAdmin)
