from django.contrib import admin

from .models import Division, Place, UserProfile, Story, Comment, Type, Question, Answer


class DivisionAdmin(admin.ModelAdmin):  # this is for to simplify urls
    prepopulated_fields = {'slug': ('title',)}


class PageAdmin(admin.ModelAdmin):  # this is for to simplify urls
    prepopulated_fields = {'slug': ('name',)}



    # custom change list creating -_-


admin.site.register(Division, DivisionAdmin)
admin.site.register(Place, PageAdmin)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Type)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProfile)
