from django.contrib import admin
from .models import User, Notes, Course, Category, Profile, Comment #  Video,
# Register your models here.
admin.site.register(User)
admin.site.register(Notes)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)