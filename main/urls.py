from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # News URLs
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/tag/<slug:tag>/', views.NewsListView.as_view(), name='news_by_tag'),
    path('news/category/<slug:category>/', views.NewsListView.as_view(), name='news_by_category'),
    
    # Programs URLs
    path('programs/', views.programs, name='programs'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
    path('programs/category/<slug:category>/', views.programs, name='programs_by_category'),
    
    # Events URLs
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/category/<slug:category>/', views.EventListView.as_view(), name='events_by_category'),
    
    # Gallery URLs
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('gallery/<slug:slug>/', views.GalleryDetailView.as_view(), name='gallery_detail'),
    
    # Editor Dashboard URLs
    path('dashboard/editor/', views.editor_dashboard, name='editor_dashboard'),
    path('dashboard/editor/news/create/', views.create_news, name='create_news'),
    path('dashboard/editor/news/edit/<int:pk>/', views.edit_news, name='edit_news'),
    path('dashboard/editor/profile/', views.user_profile, name='user_profile'),
    
    # Admin Dashboard URLs
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/programs/', views.manage_programs, name='manage_programs'),
    path('dashboard/admin/programs/create/', views.create_program, name='create_program'),
    path('dashboard/admin/programs/edit/<int:pk>/', views.edit_program, name='edit_program'),
    
    path('dashboard/admin/events/', views.manage_events, name='manage_events'),
    path('dashboard/admin/events/create/', views.create_event, name='create_event'),
    path('dashboard/admin/events/edit/<int:pk>/', views.edit_event, name='edit_event'),
    
    path('dashboard/admin/gallery/', views.manage_gallery, name='manage_gallery'),
    path('dashboard/admin/gallery/create/', views.create_gallery, name='create_gallery'),
    path('dashboard/admin/gallery/edit/<int:pk>/', views.edit_gallery, name='edit_gallery'),
    
    path('dashboard/admin/categories/', views.manage_categories, name='manage_categories'),
    path('dashboard/admin/categories/create/', views.create_category, name='create_category'),
    path('dashboard/admin/categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    
    path('dashboard/admin/tags/', views.manage_tags, name='manage_tags'),
    path('dashboard/admin/tags/create/', views.create_tag, name='create_tag'),
    path('dashboard/admin/tags/edit/<int:pk>/', views.edit_tag, name='edit_tag'),
    
    path('dashboard/admin/contacts/', views.manage_contacts, name='manage_contacts'),
    path('dashboard/admin/contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('dashboard/admin/contacts/<int:pk>/respond/', views.respond_to_contact, name='respond_to_contact'),
    
    path('dashboard/admin/users/', views.manage_users, name='manage_users'),
    path('dashboard/admin/users/<int:pk>/', views.user_detail, name='user_detail'),
    path('dashboard/admin/users/<int:pk>/edit/', views.edit_user, name='edit_user'),
]