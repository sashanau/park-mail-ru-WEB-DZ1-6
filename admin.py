from django.contrib import admin

from app.models import Profile, Question, Likes, Tag, Answer

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Likes)
admin.site.register(Tag)
admin.site.register(Answer)
