from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.sites import AdminSite
from django.http import HttpResponseForbidden
from .models import News, Program, Event, Gallery, GalleryImage, Contact

class SuperUserAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

admin_site = SuperUserAdminSite(name='superadmin')

class BaseContentAdmin(admin.ModelAdmin):
    """Base admin class for content models with common functionality"""
    list_display = ('title', 'author', 'created_at', 'is_published', 'featured')
    list_filter = ('is_published', 'featured', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'preview_image')
    
    def preview_image(self, obj):
        if obj.cover_image:
            return mark_safe(f'<img src="{obj.cover_image.url}" style="max-height: 200px;"/>')
        return "No image"
    preview_image.short_description = 'Image Preview'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new content
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.author == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.author == request.user

class NewsAdmin(BaseContentAdmin):
    list_display = BaseContentAdmin.list_display + ('views',)
    readonly_fields = BaseContentAdmin.readonly_fields + ('views',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'cover_image', 'preview_image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured', 'views', 'created_at', 'updated_at')
        }),
    )

class ProgramAdmin(BaseContentAdmin):
    list_display = ('title', 'author', 'created_at', 'is_active', 'featured', 'order')
    list_filter = ('is_active', 'featured', 'created_at', 'author')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'content', 'cover_image', 'preview_image')
        }),
        ('Settings', {
            'fields': ('is_active', 'featured', 'order', 'created_at', 'updated_at')
        }),
    )

class EventAdmin(BaseContentAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'is_published', 'registration_required')
    list_filter = ('is_published', 'featured', 'registration_required', 'start_date')
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'slug', 'description', 'content', 'cover_image', 'preview_image')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Registration', {
            'fields': ('registration_required', 'max_participants')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured', 'created_at', 'updated_at')
        }),
    )

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'caption', 'order')

class GalleryAdmin(BaseContentAdmin):
    inlines = [GalleryImageInline]
    fieldsets = (
        ('Gallery Details', {
            'fields': ('title', 'slug', 'description', 'cover_image', 'preview_image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured', 'created_at', 'updated_at')
        }),
    )

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete contact entries

# Register models with our custom admin site
admin_site.register(News, NewsAdmin)
admin_site.register(Program, ProgramAdmin)
admin_site.register(Event, EventAdmin)
admin_site.register(Gallery, GalleryAdmin)
admin_site.register(Contact, ContactAdmin)

# Set admin site branding
admin_site.site_header = 'Ministry of Youth and Sports Development Admin'
admin_site.site_title = 'Ministry Admin Portal'
admin_site.index_title = 'Content Management'
