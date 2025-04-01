from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates test users for development'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Create Editor group if it doesn't exist
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        
        # Create test users
        users_data = [
            {
                'username': 'editor',
                'email': 'editor@example.com',
                'password': 'editor123',
                'is_staff': False,
                'is_superuser': False,
                'groups': [editor_group],
            },
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': False,
                'groups': [],
            },
            {
                'username': 'superadmin',
                'email': 'superadmin@example.com',
                'password': 'superadmin123',
                'is_staff': True,
                'is_superuser': True,
                'groups': [],
            },
        ]

        for user_data in users_data:
            groups = user_data.pop('groups')
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(**user_data)
                user.groups.set(groups)
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
            else:
                self.stdout.write(f'User {user_data["username"]} already exists')
