from django import forms
from django.contrib.auth.models import User
from .models import News, Program, Event, UserProfile, Category, Tag, Contact, Gallery, GalleryImage

class NewsForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select w-full rounded-lg'}),
        required=False
    )

    class Meta:
        model = News
        fields = ['title', 'cover_image', 'content', 'excerpt', 'category', 'tags', 
                 'is_published', 'featured', 'meta_description', 'meta_keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'content': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select w-full rounded-lg'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'cover_image', 'description', 'content', 'category', 
                 'is_active', 'featured', 'order', 'start_date', 'end_date',
                 'registration_open', 'max_participants', 'requirements', 
                 'location', 'price', 'meta_description', 'meta_keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-select w-full rounded-lg'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control w-full rounded-lg', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control w-full rounded-lg', 'type': 'date'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'price': forms.NumberInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'cover_image', 'description', 'content', 'category',
                 'start_date', 'end_date', 'location', 'is_published', 'featured',
                 'registration_required', 'max_participants', 'status', 'price',
                 'meta_description', 'meta_keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-select w-full rounded-lg'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control w-full rounded-lg', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control w-full rounded-lg', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'status': forms.Select(attrs={'class': 'form-select w-full rounded-lg'}),
            'price': forms.NumberInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'position', 'phone', 'social_links']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'bio': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 4}),
            'position': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'phone': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'social_links': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3})
        }

    def clean_social_links(self):
        try:
            import json
            data = json.loads(self.cleaned_data['social_links'])
            return data
        except:
            return {}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'order': forms.NumberInput(attrs={'class': 'form-control w-full rounded-lg'})
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'subject': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'message': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 5})
        }

class ContactResponseForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['response_message']
        widgets = {
            'response_message': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 5})
        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'cover_image', 'category', 
                 'is_published', 'featured', 'meta_description', 'meta_keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 3}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'category': forms.Select(attrs={'class': 'form-select w-full rounded-lg'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control w-full rounded-lg', 'rows': 2}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'})
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'caption': forms.TextInput(attrs={'class': 'form-control w-full rounded-lg'}),
            'order': forms.NumberInput(attrs={'class': 'form-control w-full rounded-lg'})
        }
