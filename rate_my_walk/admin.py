from django.contrib import admin
from rate_my_walk.models import WalkPage, Rating, Comment, Photo, UserProfile

admin.site.register(WalkPage)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(UserProfile)


