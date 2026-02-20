from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User, Idea, CollaborationRequest, ChatMessage
from .context_processors import RESEARCH_FIELDS  # if needed in views

def send_email_notification(subject, recipient_email, body):
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL or 'noreply@peermatch.com',
            [recipient_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"[Email Error] {e}")

def index(request):
    ideas = Idea.objects.all().order_by('-date_posted')
    return render(request, 'index.html', {'ideas': ideas})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')
        
        # Create user
        # We set username to email to ensure uniqueness if not provided, or handle it otherwise.
        # CustomUser uses username by default. We can use email as username or generate one.
        username = email
        if User.objects.filter(username=username).exists():
             import uuid
             username = f"{email}_{uuid.uuid4().hex[:6]}"

        user = User.objects.create_user(username=username, email=email, password=password)
        user.name = name
        user.institution = request.POST.get('institution')
        user.research_field = request.POST.get('research_field')
        user.interests = request.POST.get('interests')
        user.skillset = request.POST.get('skillset')
        user.education = request.POST.get('education')
        user.experience = request.POST.get('experience')
        user.save()
        
        messages.success(request, 'Account created! Please sign in.')
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    email_value = ''
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        email_value = email
        
        # Authenticate by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            if user.status == 'blocked':
                messages.error(request, 'Your account has been blocked.')
                return render(request, 'login.html', {'email_value': email_value})
            
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')
            
    return render(request, 'login.html', {'email_value': email_value})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def researchers(request):
    q = request.GET.get('q', '').strip()
    field = request.GET.get('field', '').strip()
    
    users = User.objects.filter(~Q(role='admin'))
    
    if q:
        users = users.filter(Q(name__icontains=q) | Q(institution__icontains=q))
    if field:
        users = users.filter(research_field=field)
        
    users = users.order_by('name')
    return render(request, 'researchers.html', {'users': users, 'q': q, 'field': field})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    collab_count = CollaborationRequest.objects.filter(idea=idea, status='Accepted').count()
    return render(request, 'idea_detail.html', {'idea': idea, 'collab_count': collab_count})

@login_required
def new_idea(request):
    if request.method == 'POST':
        Idea.objects.create(
            author=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            field=request.POST.get('field'),
            keywords=request.POST.get('keywords'),
            progress=request.POST.get('progress'),
            help_needed=request.POST.get('help_needed'),
            skills_needed=request.POST.get('skills_needed'),
            expertise_needed=request.POST.get('expertise_needed')
        )
        messages.success(request, 'Idea posted!')
        return redirect('my_profile')
    return render(request, 'idea_form.html', {'action': 'Post New'})

@login_required
def edit_idea(request, id):
    idea = get_object_or_404(Idea, id=id)
    if idea.author != request.user:
        messages.error(request, 'Unauthorized')
        return redirect('my_profile')
        
    if request.method == 'POST':
        idea.title = request.POST.get('title')
        idea.description = request.POST.get('description')
        idea.field = request.POST.get('field')
        idea.keywords = request.POST.get('keywords')
        idea.progress = request.POST.get('progress')
        idea.help_needed = request.POST.get('help_needed')
        idea.skills_needed = request.POST.get('skills_needed')
        idea.expertise_needed = request.POST.get('expertise_needed')
        idea.save()
        messages.success(request, 'Idea updated!')
        return redirect('idea_detail', idea_id=idea.id)
    return render(request, 'idea_form.html', {'action': 'Edit', 'idea': idea})

@login_required
def delete_idea(request, id):
    idea = get_object_or_404(Idea, id=id)
    if idea.author != request.user and request.user.role != 'admin':
        messages.error(request, 'Unauthorized')
        return redirect('my_profile')
    
    idea.delete()
    messages.info(request, 'Idea deleted.')
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('my_profile')

@login_required
def request_collab(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if idea.author == request.user:
        messages.warning(request, "Can't collaborate on your own idea!")
        return redirect('idea_detail', idea_id=idea_id)
        
    if CollaborationRequest.objects.filter(idea=idea, from_user=request.user).exists():
        messages.info(request, "Request already sent.")
        return redirect('idea_detail', idea_id=idea_id)
        
    CollaborationRequest.objects.create(idea=idea, from_user=request.user, to_user=idea.author)
    
    send_email_notification(
        f"[PeerMatch] New Collaboration Request on '{idea.title}'",
        idea.author.email,
        f"Hello {idea.author.name},\n\n{request.user.name} wants to collaborate on '{idea.title}'.\n\nLog in: http://127.0.0.1:8000/my-profile\n\n— PeerMatch Team"
    )
    messages.success(request, "Collaboration request sent!")
    return redirect('idea_detail', idea_id=idea_id)

@login_required
def respond_request(request, req_id, status):
    req = get_object_or_404(CollaborationRequest, id=req_id)
    if req.to_user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('my_profile')
        
    if status in ['Accepted', 'Rejected']:
        req.status = status
        req.save()
        messages.success(request, f"Request {status.lower()}!")
        
        send_email_notification(
            f"[PeerMatch] Your request was {status}",
            req.from_user.email,
            f"Hello {req.from_user.name},\n\n{request.user.name} has {status.lower()} your request on '{req.idea.title}'.\n\nhttp://127.0.0.1:8000/my-profile\n\n— PeerMatch Team"
        )
    return redirect('my_profile')

@login_required
def my_profile(request):
    ideas = Idea.objects.filter(author=request.user).order_by('-date_posted')
    sent = CollaborationRequest.objects.filter(from_user=request.user)
    received = CollaborationRequest.objects.filter(to_user=request.user)
    accepted_collabs = CollaborationRequest.objects.filter(
        (Q(to_user=request.user) | Q(from_user=request.user)) & Q(status='Accepted')
    ).count()
    pending_received_count = received.filter(status='Pending').count()
    
    return render(request, 'my_profile.html', {
        'user': request.user,
        'ideas': ideas,
        'sent': sent,
        'received': received,
        'accepted_collabs': accepted_collabs,
        'pending_received_count': pending_received_count
    })

@login_required
def profile(request, user_id):
    if user_id == request.user.id:
        return redirect('my_profile')
    
    user = get_object_or_404(User, id=user_id)
    ideas = Idea.objects.filter(author=user).order_by('-date_posted')
    accepted_collabs = CollaborationRequest.objects.filter(
        (Q(to_user=user) | Q(from_user=user)) & Q(status='Accepted')
    ).count()
    
    return render(request, 'profile.html', {
        'user': user,
        'ideas': ideas,
        'accepted_collabs': accepted_collabs
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name')
        user.institution = request.POST.get('institution')
        user.research_field = request.POST.get('research_field')
        user.interests = request.POST.get('interests')
        user.skillset = request.POST.get('skillset')
        user.education = request.POST.get('education')
        user.experience = request.POST.get('experience')
        user.previous_work = request.POST.get('previous_work')
        user.ongoing_work = request.POST.get('ongoing_work')
        
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
            
        user.save()
        messages.success(request, 'Profile updated!')
        return redirect('my_profile')
    return render(request, 'edit_profile.html')

@login_required
def messages_view(request):
    sent = ChatMessage.objects.filter(sender=request.user).values_list('recipient_id', flat=True).distinct()
    received = ChatMessage.objects.filter(recipient=request.user).values_list('sender_id', flat=True).distinct()
    
    partner_ids = set(list(sent) + list(received))
    partners = User.objects.filter(id__in=partner_ids)
    
    return render(request, 'messages.html', {
        'partners': partners,
        'active_user': None,
        'conversation': []
    })

@login_required
def conversation(request, user_id):
    other = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            ChatMessage.objects.create(sender=request.user, recipient=other, content=content)
        return redirect('conversation', user_id=user_id)
        
    # Mark read
    ChatMessage.objects.filter(sender=other, recipient=request.user, read=False).update(read=True)
    
    conv = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient=other)) |
        (Q(sender=other) & Q(recipient=request.user))
    ).order_by('timestamp')
    
    sent = ChatMessage.objects.filter(sender=request.user).values_list('recipient_id', flat=True).distinct()
    received = ChatMessage.objects.filter(recipient=request.user).values_list('sender_id', flat=True).distinct()
    partner_ids = set(list(sent) + list(received))
    partner_ids.add(user_id)
    
    partners = User.objects.filter(id__in=partner_ids)
    
    return render(request, 'messages.html', {
        'partners': partners,
        'active_user': other,
        'conversation': conv
    })

@login_required
def api_messages(request, user_id):
    after_id = int(request.GET.get('after', 0))
    msgs = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient_id=user_id)) |
        (Q(sender_id=user_id) & Q(recipient=request.user)),
        id__gt=after_id
    ).order_by('timestamp')
    
    ChatMessage.objects.filter(sender_id=user_id, recipient=request.user, read=False).update(read=True)
    
    data = [{
        'id': m.id,
        'content': m.content,
        'mine': m.sender == request.user,
        'time': m.timestamp.strftime('%H:%M')
    } for m in msgs]
    
    return JsonResponse(data, safe=False)

@login_required
def api_send_message(request):
    pass # Implementation omitted for simplicity, but can be added if frontend uses it. 
    # Since existing provided Flask code uses POST form submission for messages in `conversation` view,
    # and also has an API endpoint, we'll assume the API might be used by JS polling.
    # The Flask code has `request.get_json()`.
    
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        content = (data.get('content') or '').strip()
        recipient_id = data.get('user_id')
        if not content:
            return JsonResponse({'error': 'Empty'}, status=400)
            
        recipient = get_object_or_404(User, id=recipient_id)
        msg = ChatMessage.objects.create(sender=request.user, recipient=recipient, content=content)
        
        return JsonResponse({'id': msg.id, 'time': msg.timestamp.strftime('%H:%M')})
    return JsonResponse({'error': 'POST required'}, status=405)

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, "Access Denied")
        return redirect('index')
        
    return render(request, 'admin.html', {
        'users': User.objects.order_by('-role', 'name'),
        'ideas': Idea.objects.order_by('-date_posted'),
        'collabs': CollaborationRequest.objects.order_by('-timestamp'),
        'user_count': User.objects.count(),
        'idea_count': Idea.objects.count(),
        'collab_count': CollaborationRequest.objects.filter(status='Accepted').count()
    })

@login_required
def block_user(request, user_id):
    if request.user.role != 'admin':
        return redirect('index')
    user = get_object_or_404(User, id=user_id)
    user.status = 'blocked' if user.status == 'active' else 'active'
    user.save()
    return redirect('admin_dashboard')

@login_required
def make_admin(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, "Access Denied")
        return redirect('index')
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.warning(request, "You cannot change your own role.")
        return redirect('admin_dashboard')
        
    user.role = 'user' if user.role == 'admin' else 'admin'
    user.save()
    messages.success(request, f"{user.name} is now {'an Admin' if user.role == 'admin' else 'a regular User'}.")
    return redirect('admin_dashboard')
