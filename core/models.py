from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    # AbstractUser already has username, email, first_name, last_name, password, is_staff, is_active, date_joined
    # We map 'name' to first_name usually, or add a 'full_name' field. The existing app uses 'name'.
    # We'll add a 'name' field for compatibility, or use 'get_full_name'.
    # Existing app: name, email, institution, research_field, interests, role, status, profile_pic, skillset, education, experience, previous_work, ongoing_work
    
    name = models.CharField(max_length=100)  # separate from username? We can make username=email or auto-generate.
    institution = models.CharField(max_length=150, blank=True, null=True)
    research_field = models.CharField(max_length=100, blank=True, null=True)
    interests = models.CharField(max_length=500, blank=True, null=True)
    role = models.CharField(max_length=20, default='user')  # 'user', 'admin'
    status = models.CharField(max_length=20, default='active')  # 'active', 'blocked'
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    skillset = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    previous_work = models.TextField(blank=True, null=True)
    ongoing_work = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or self.username

    @property
    def interests_list(self):
        return [x.strip() for x in self.interests.split(',')] if self.interests else []

    @property
    def skillset_list(self):
        return [x.strip() for x in self.skillset.split(',')] if self.skillset else []

class Idea(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    title = models.CharField(max_length=200)
    description = models.TextField()
    field = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    progress = models.TextField(blank=True, null=True)
    help_needed = models.TextField(blank=True, null=True)
    skills_needed = models.CharField(max_length=300, blank=True, null=True)
    expertise_needed = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def keywords_list(self):
        return [x.strip() for x in self.keywords.split(',')] if self.keywords else []

    @property
    def skills_needed_list(self):
        return [x.strip() for x in self.skills_needed.split(',')] if self.skills_needed else []

    @property
    def expertise_needed_list(self):
        return [x.strip() for x in self.expertise_needed.split(',')] if self.expertise_needed else []

class CollaborationRequest(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='requests')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, default='Pending')  # 'Pending', 'Accepted', 'Rejected'
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Request from {self.from_user} to {self.to_user} on {self.idea}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"
