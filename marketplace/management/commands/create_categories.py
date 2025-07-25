from django.core.management.base import BaseCommand
from marketplace.models import Category

class Command(BaseCommand):
    help = 'Create default categories for the marketplace site'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Home & Garden', 'description': 'Furniture, appliances, home decor, and garden items'},
            {'name': 'Electronics', 'description': 'Phones, computers, gaming, audio, and tech gadgets'},
            {'name': 'Fashion & Clothing', 'description': 'Clothing, shoes, accessories, and jewelry'},
            {'name': 'Food & Drinks', 'description': 'Gourmet foods, beverages, and specialty ingredients'},
            {'name': 'Sports & Outdoors', 'description': 'Sports equipment, outdoor gear, and fitness items'},
            {'name': 'Books & Media', 'description': 'Books, movies, music, and educational materials'},
            {'name': 'Toys & Games', 'description': 'Toys, board games, video games, and collectibles'},
            {'name': 'Health & Beauty', 'description': 'Skincare, cosmetics, health supplements, and wellness products'},
            {'name': 'Automotive', 'description': 'Car parts, accessories, tools, and vehicle-related items'},
            {'name': 'Art & Collectibles', 'description': 'Artwork, antiques, collectibles, and vintage items'},
        ]

        created_count = 0
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        )
