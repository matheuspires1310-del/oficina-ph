from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cria superusuário automaticamente'

    def handle(self, *args, **options):
        User = get_user_model()

        email = "matheuspires1310@gmail.com"
        username = "admin"
        password = "132206"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário já existe'))
