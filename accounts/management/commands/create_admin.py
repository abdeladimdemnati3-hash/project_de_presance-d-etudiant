from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import Utilisateur


class Command(BaseCommand):
    help = 'Create default admin user for Heroku deployment'

    def handle(self, *args, **options):
        username = 'admin'
        password = getattr(settings, '_HEROKU_ADMIN_PASSWORD', 'Admin1234!')

        import os
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin1234!')

        user, created = Utilisateur.objects.get_or_create(
            username=username,
            defaults={
                'email': 'admin@admin.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user created (password: {password})'))
        else:
            # Ensure existing admin has correct role
            if user.role != 'admin':
                user.role = 'admin'
                user.is_staff = True
                user.is_superuser = True
                user.save(update_fields=['role', 'is_staff', 'is_superuser'])
                self.stdout.write(self.style.SUCCESS('Admin user role updated to admin'))
            else:
                self.stdout.write('Admin user already exists with correct role.')
