from django.contrib import admin
from .models import Division,Page,like,image,Story


class DivisionAdmin(admin.ModelAdmin):          # this is for to simplify urls
    prepopulated_fields = {'slug':('title',)}
class PageAdmin(admin.ModelAdmin):          # this is for to simplify urls
    prepopulated_fields = {'slug':('name',)}



admin.site.register(Division,DivisionAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(like)
admin.site.register(image)
admin.site.register(Story)
