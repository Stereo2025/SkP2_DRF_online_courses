from django.contrib import admin

from lessons.models import Course, Lesson


@admin.register(Course)
class ContactAdmin(admin.ModelAdmin):
    """Админка Course"""
    list_display = ('id', 'name', 'image', 'description', 'date_modified')


@admin.register(Lesson)
class ContactAdmin(admin.ModelAdmin):
    """Админка Lesson"""
    list_display = ('id', 'name', 'image', 'description', 'video_url', 'date_modified')
