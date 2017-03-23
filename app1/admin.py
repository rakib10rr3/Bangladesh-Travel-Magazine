from django.contrib import admin

from .models import Division, Place, Story, Comment, Type


class DivisionAdmin(admin.ModelAdmin):          # this is for to simplify urls
    prepopulated_fields = {'slug':('title',)}
class PageAdmin(admin.ModelAdmin):          # this is for to simplify urls
    prepopulated_fields = {'slug':('name',)}




admin.site.register(Division,DivisionAdmin)
admin.site.register(Place, PageAdmin)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Type)
