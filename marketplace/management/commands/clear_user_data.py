from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Listing, Purchase, Watchlist

User = get_user_model()

class Command(BaseCommand):
    help = 'Clear all user data and listings while preserving categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all user data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This command will delete ALL users, listings, purchases, and watchlist items.\n'
                    'Categories will be preserved.\n'
                    'To proceed, run: python manage.py clear_user_data --confirm'
                )
            )
            return

        self.stdout.write('Starting data cleanup...')

        # Delete purchases first (foreign key dependencies)
        purchase_count = Purchase.objects.count()
        Purchase.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {purchase_count} purchases')
        )

        # Delete watchlist items
        watchlist_count = Watchlist.objects.count()
        Watchlist.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {watchlist_count} watchlist items')
        )

        # Delete listings
        listing_count = Listing.objects.count()
        Listing.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {listing_count} listings')
        )

        # Delete all users except superusers (to preserve admin access)
        regular_user_count = User.objects.filter(is_superuser=False).count()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {regular_user_count} regular users')
        )

        superuser_count = User.objects.filter(is_superuser=True).count()
        self.stdout.write(
            self.style.WARNING(f'Preserved {superuser_count} superuser(s) for admin access')
        )

        self.stdout.write(
            self.style.SUCCESS('Data cleanup completed successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS('Categories have been preserved.')
        )
