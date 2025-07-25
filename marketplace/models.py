from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=200, blank=True, null=True)
    imageFile = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    quantity_sold = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    isSold = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='category_listings')
    sold_at = models.DateTimeField(null=True, blank=True)

    def get_image_url(self):
        """Return the appropriate image URL - prioritize uploaded file over URL"""
        if self.imageFile:
            return self.imageFile.url
        elif self.imageUrl:
            return self.imageUrl
        else:
            return None

    def is_available(self):
        """Check if the listing is available for purchase"""
        return self.isActive and self.quantity_available() > 0

    def quantity_available(self):
        """Return the number of items still available for purchase"""
        return max(0, self.quantity - self.quantity_sold)

    def mark_sale(self, quantity_purchased=1):
        """Mark items as sold and update status"""
        self.quantity_sold += quantity_purchased
        if self.quantity_sold >= self.quantity:
            self.isSold = True
            self.sold_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Purchase(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    quantity_purchased = models.PositiveIntegerField(default=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} purchased {self.quantity_purchased}x {self.listing.title} for ${self.total_price}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} watching {self.listing.title}"