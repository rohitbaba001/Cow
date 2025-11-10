from django.core.management.base import BaseCommand
from core.models import User
import os


class Command(BaseCommand):
    help = 'Creates a default superuser if none exists'

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(user_type='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists. Skipping creation.'))
            return

        # Get credentials from environment variables or use defaults
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                password=password,
                user_type='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
            self.stdout.write(self.style.WARNING(f'Default password: {password}'))
            self.stdout.write(self.style.WARNING('Please change the password after first login!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
