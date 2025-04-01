from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import News, Program, Event, UserProfile, Category, Tag, Contact, Gallery, GalleryImage
from .forms import (
    NewsForm, ProgramForm, EventForm, UserProfileForm, CategoryForm, 
    TagForm, ContactForm, ContactResponseForm, GalleryForm, GalleryImageForm
)

def home(request):
    featured_news = News.objects.filter(is_published=True, featured=True)[:3]
    featured_programs = Program.objects.filter(is_active=True, featured=True)[:3]
    featured_events = Event.objects.filter(is_published=True, featured=True)[:3]
    featured_galleries = Gallery.objects.filter(is_published=True, featured=True)[:3]
    
    context = {
        'featured_news': featured_news,
        'featured_programs': featured_programs,
        'featured_events': featured_events,
        'featured_galleries': featured_galleries,
    }
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

class NewsListView(ListView):
    model = News
    template_name = 'main/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        tag = self.kwargs.get('tag')
        category = self.kwargs.get('category')
        
        if tag:
            queryset = queryset.filter(tags__name=tag)
        if category:
            queryset = queryset.filter(category__name=category)
            
        return queryset.order_by('-created_at')

class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context

def programs(request, category=None):
    programs_list = Program.objects.filter(is_active=True)
    if category:
        programs_list = programs_list.filter(category__name=category)
    
    context = {
        'programs': programs_list,
        'categories': Category.objects.annotate(program_count=Count('programs'))
    }
    return render(request, 'main/programs.html', context)

def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    context = {
        'program': program,
        'related_programs': Program.objects.filter(
            category=program.category
        ).exclude(id=program.id)[:3]
    }
    return render(request, 'main/program_detail.html', context)

class EventListView(ListView):
    model = Event
    template_name = 'main/event_list.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True)
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset.order_by('start_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'main/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_events'] = Event.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context

class GalleryListView(ListView):
    model = Gallery
    template_name = 'main/gallery_list.html'
    context_object_name = 'galleries'
    paginate_by = 12
    
    def get_queryset(self):
        return Gallery.objects.filter(is_published=True).order_by('-created_at')

class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'main/gallery_detail.html'
    context_object_name = 'gallery'

@login_required
def editor_dashboard(request):
    user_news = News.objects.filter(author=request.user)
    draft_count = user_news.filter(is_published=False).count()
    published_count = user_news.filter(is_published=True).count()
    recent_news = user_news.order_by('-created_at')[:5]
    
    context = {
        'draft_count': draft_count,
        'published_count': published_count,
        'recent_news': recent_news,
        'total_views': sum(news.views for news in user_news),
    }
    return render(request, 'main/editor_dashboard.html', context)

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            form.save_m2m()  # Save tags
            messages.success(request, 'News article created successfully!')
            return redirect('editor_dashboard')
    else:
        form = NewsForm()
    return render(request, 'main/news_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk, author=request.user)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News article updated successfully!')
            return redirect('editor_dashboard')
    else:
        form = NewsForm(instance=news)
    return render(request, 'main/news_form.html', {'form': form, 'action': 'Edit'})

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'main/user_profile.html', {'form': form})

@login_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_news': News.objects.count(),
        'total_programs': Program.objects.count(),
        'total_events': Event.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_news': News.objects.order_by('-created_at')[:5],
        'recent_contacts': Contact.objects.filter(response_message='').order_by('-created_at')[:5],
    }
    return render(request, 'main/admin_dashboard.html', context)

@login_required
def manage_programs(request):
    programs = Program.objects.all().order_by('-created_at')
    return render(request, 'main/manage_programs.html', {'programs': programs})

@login_required
def create_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program created successfully!')
            return redirect('manage_programs')
    else:
        form = ProgramForm()
    return render(request, 'main/program_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_program(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully!')
            return redirect('manage_programs')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'main/program_form.html', {'form': form, 'action': 'Edit'})

@login_required
def manage_events(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'main/manage_events.html', {'events': events})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('manage_events')
    else:
        form = EventForm()
    return render(request, 'main/event_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'main/event_form.html', {'form': form, 'action': 'Edit'})

@login_required
def manage_gallery(request):
    galleries = Gallery.objects.all().order_by('-created_at')
    return render(request, 'main/manage_gallery.html', {'galleries': galleries})

@login_required
def create_gallery(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('gallery_images')
            for index, image in enumerate(images):
                GalleryImage.objects.create(
                    gallery=gallery,
                    image=image,
                    order=index + 1
                )
            
            messages.success(request, 'Gallery created successfully!')
            return redirect('manage_gallery')
    else:
        form = GalleryForm()
    return render(request, 'main/gallery_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_gallery(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('gallery_images')
            for index, image in enumerate(images):
                GalleryImage.objects.create(
                    gallery=gallery,
                    image=image,
                    order=gallery.images.count() + index + 1
                )
            
            messages.success(request, 'Gallery updated successfully!')
            return redirect('manage_gallery')
    else:
        form = GalleryForm(instance=gallery)
    return render(request, 'main/gallery_form.html', {
        'form': form,
        'action': 'Edit',
        'gallery': gallery
    })

@login_required
def manage_categories(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'main/manage_categories.html', {'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'main/category_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'main/category_form.html', {
        'form': form,
        'action': 'Edit',
        'category': category
    })

@login_required
def manage_tags(request):
    tags = Tag.objects.all()
    return render(request, 'main/manage_tags.html', {'tags': tags})

@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('manage_tags')
    else:
        form = TagForm()
    return render(request, 'main/tag_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated successfully!')
            return redirect('manage_tags')
    else:
        form = TagForm(instance=tag)
    return render(request, 'main/tag_form.html', {
        'form': form,
        'action': 'Edit',
        'tag': tag
    })

@login_required
def manage_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'main/manage_contacts.html', {'contacts': contacts})

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'main/contact_detail.html', {'contact': contact})

@login_required
def respond_to_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactResponseForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.responded_at = timezone.now()
            contact.save()
            messages.success(request, 'Response sent successfully!')
            return redirect('manage_contacts')
    else:
        form = ContactResponseForm(instance=contact)
    return render(request, 'main/contact_response.html', {
        'form': form,
        'contact': contact
    })

@login_required
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'main/manage_users.html', {'users': users})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/user_detail.html', {'user_detail': user})

@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated successfully!')
            return redirect('manage_users')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'main/user_form.html', {
        'form': form,
        'user_detail': user
    })
