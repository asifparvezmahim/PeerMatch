from django.contrib import admin
from .models import User, Idea, CollaborationRequest, ChatMessage

admin.site.register(User)
admin.site.register(Idea)
admin.site.register(CollaborationRequest)
admin.site.register(ChatMessage)
