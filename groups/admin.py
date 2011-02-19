from django.contrib import admin
from models import InterestGroup, Membership

class MembershipsInline(admin.TabularInline):
    model = Membership

class InterestGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = (MembershipsInline, )


admin.site.register(InterestGroup, InterestGroupAdmin)
