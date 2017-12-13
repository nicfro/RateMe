from django.contrib import admin

# Register your models here.
from vote.models import Image, Vote, Elo, Report


class DefaultAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ("uploaded",)

admin.site.register(Image, ImageAdmin)
admin.site.register(Vote, DefaultAdmin)
admin.site.register(Elo, DefaultAdmin)
admin.site.register(Report, DefaultAdmin)
