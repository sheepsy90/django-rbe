from django.core.management import BaseCommand
from skills.models import UserSkill, UserSlugs



class Command(BaseCommand):
    help = 'Move the old slugs to the new ones'

    def handle(self, *args, **options):
        for user_slug in UserSlugs.objects.all():
            UserSkill.objects.get_or_create(user=user_slug.user, slug=user_slug.slug, level=3)

