from django.contrib import admin
from models import InterestGroup, Membership, Event, Talk

class MembershipsInline(admin.TabularInline):
    model = Membership

class InterestGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = (MembershipsInline, )

class TalksInline(admin.StackedInline):
    model = Talk


class EventAdmin(admin.ModelAdmin):
    inlines = (TalksInline, )

admin.site.register(InterestGroup, InterestGroupAdmin)
admin.site.register(Event, EventAdmin)
