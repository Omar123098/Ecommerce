from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone

from .models import Listing, User, Category, Watchlist, Purchase


def index(request):
    # Get all categories for the filter
    categories = Category.objects.all()
    
    # Get all available listings (active and not sold)
    listings = Listing.objects.filter(isActive=True, isSold=False).order_by('-created_at')
    
    # Filter by category if specified
    if request.method == 'GET':
        category_id = request.GET.get('category', None)
        if category_id:
            listings = listings.filter(category_id=category_id)

    return render(request, "marketplace/index.html", {
        "listings": listings,
        "categories": categories
    })

def category_listings(request, category_id):
    # Get the category object
    category = Category.objects.get(id=category_id)
    
    # Get all available listings in this category (active and not sold)
    listings = Listing.objects.filter(category=category, isActive=True, isSold=False).order_by('-created_at')

    return render(request, "marketplace/category_listings.html", {
        "listings": listings,
        "category": category
    })

def create_listing(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "marketplace/create_listing.html", {
            "categories": categories,
            "message": None
        })
    elif request.method == 'POST':
        title = request.POST["title"]
        imageUrl = request.POST.get("imageUrl", "")
        imageFile = request.FILES.get("imageFile", None)
        description = request.POST["description"]
        price = request.POST["price"]
        quantity = request.POST.get("quantity", "1")
        category_id = request.POST.get("category", None)

        # Validate price
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
        except ValueError as e:
            categories = Category.objects.all()
            return render(request, "marketplace/create_listing.html", {
                "categories": categories,
                "message": str(e)
            })

        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be at least 1.")
        except ValueError as e:
            categories = Category.objects.all()
            return render(request, "marketplace/create_listing.html", {
                "categories": categories,
                "message": str(e)
            })

        # Create the listing
        listing = Listing(
            title=title,
            imageUrl=imageUrl,
            imageFile=imageFile,
            description=description,
            price=price,
            quantity=quantity,
            owner=request.user,
            category_id=category_id
        )
        listing.save()

        return HttpResponseRedirect(reverse("index"))

def listing_detail(request, listing_id):
    # Get the listing object
    listing = get_object_or_404(Listing, id=listing_id)

    # Check if the listing is available - allow viewing sold items
    if not listing.isActive and not listing.isSold and (not request.user.is_authenticated or listing.owner != request.user):
        return HttpResponse("This listing is no longer active.", status=404)

    # Handle purchase request
    if request.method == 'POST' and 'purchase' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to purchase items.")
            return redirect('login')
        
        if request.user == listing.owner:
            messages.error(request, "You cannot purchase your own listing.")
        elif not listing.is_available():
            messages.error(request, "This item is no longer available for purchase.")
        else:
            try:
                # Get quantity from form, default to 1
                quantity_requested = int(request.POST.get('quantity', 1))
                
                # Validate quantity
                if quantity_requested <= 0:
                    messages.error(request, "Quantity must be at least 1.")
                elif quantity_requested > listing.quantity_available():
                    messages.error(request, f"Only {listing.quantity_available()} item(s) available.")
                else:
                    # Calculate total price
                    total_price = listing.price * quantity_requested
                    
                    # Create the purchase
                    purchase = Purchase.objects.create(
                        listing=listing,
                        buyer=request.user,
                        seller=listing.owner,
                        quantity_purchased=quantity_requested,
                        purchase_price=listing.price,
                        total_price=total_price
                    )
                    
                    # Update listing quantity and status
                    listing.mark_sale(quantity_requested)
                    
                    if quantity_requested == 1:
                        messages.success(request, f"Congratulations! You have successfully purchased '{listing.title}' for ${total_price}.")
                    else:
                        messages.success(request, f"Congratulations! You have successfully purchased {quantity_requested}x '{listing.title}' for ${total_price}.")
                    
                    return redirect('listing_detail', listing_id=listing.id)
                    
            except ValueError:
                messages.error(request, "Please enter a valid quantity.")
            except Exception as e:
                messages.error(request, "An error occurred while processing your purchase.")
    
    # Check if user has this item in watchlist
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    # Get purchase information if sold
    purchase = None
    if listing.isSold:
        try:
            purchase = Purchase.objects.get(listing=listing)
        except Purchase.DoesNotExist:
            pass

    return render(request, "marketplace/listing_detail.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "purchase": purchase,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "marketplace/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "marketplace/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "marketplace/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "marketplace/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "marketplace/register.html")


@login_required
def profile(request):
    """User profile page showing their listings, purchases, and watchlist summary"""
    user = request.user
    
    # Get user's listings
    user_listings = Listing.objects.filter(owner=user).order_by('-created_at')
    
    # Get user's recent purchases
    user_purchases = Purchase.objects.filter(buyer=user).order_by('-purchase_date')[:5]
    
    # Get user's recent sales
    user_sales = Purchase.objects.filter(seller=user).order_by('-purchase_date')[:5]
    
    # Get user's watchlist count
    watchlist_count = Watchlist.objects.filter(user=user).count()
    
    # Get total purchases made
    total_purchases = Purchase.objects.filter(buyer=user).count()
    
    # Get total sales made
    total_sales = Purchase.objects.filter(seller=user).count()
    
    return render(request, "marketplace/profile.html", {
        "user_listings": user_listings,
        "user_purchases": user_purchases,
        "user_sales": user_sales,
        "watchlist_count": watchlist_count,
        "total_purchases": total_purchases,
        "total_sales": total_sales,
    })


@login_required
def watchlist(request):
    """Display user's watchlist"""
    user_watchlist = Watchlist.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, "marketplace/watchlist.html", {
        "watchlist": user_watchlist
    })


@login_required
def my_purchases(request):
    """Display user's purchase history"""
    user_purchases = Purchase.objects.filter(buyer=request.user).order_by('-purchase_date')
    
    return render(request, "marketplace/my_purchases.html", {
        "purchases": user_purchases
    })


@login_required
def add_to_watchlist(request, listing_id):
    """Add a listing to user's watchlist"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if already in watchlist
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    
    if created:
        messages.success(request, f"Added '{listing.title}' to your watchlist!")
    else:
        messages.info(request, f"'{listing.title}' is already in your watchlist.")
    
    return redirect('listing_detail', listing_id=listing_id)


@login_required
def remove_from_watchlist(request, listing_id):
    """Remove a listing from user's watchlist"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    try:
        watchlist_item = Watchlist.objects.get(user=request.user, listing=listing)
        watchlist_item.delete()
        messages.success(request, f"Removed '{listing.title}' from your watchlist!")
    except Watchlist.DoesNotExist:
        messages.error(request, "This listing was not in your watchlist.")
    
    return redirect('listing_detail', listing_id=listing_id)


@login_required
def edit_listing(request, listing_id):
    """Edit a listing (only by owner)"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if user is the owner
    if listing.owner != request.user:
        messages.error(request, "You can only edit your own listings.")
        return redirect('listing_detail', listing_id=listing_id)
    
    # Check if listing is still active and not sold
    if not listing.isActive or listing.isSold:
        messages.error(request, "You cannot edit a sold or closed listing.")
        return redirect('listing_detail', listing_id=listing_id)
    
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "marketplace/edit_listing.html", {
            "listing": listing,
            "categories": categories,
        })
    
    elif request.method == 'POST':
        # Get form data
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category_id = request.POST.get("category")
        image_type = request.POST.get("image_type", "file")
        image_file = request.FILES.get("imageFile")
        image_url = request.POST.get("imageUrl", "").strip()
        
        # Validate data
        if not title or not description or not price:
            messages.error(request, "All fields are required.")
            return redirect('edit_listing', listing_id=listing_id)
        
        try:
            price = float(price)
            if price <= 0:
                messages.error(request, "Price must be greater than 0.")
                return redirect('edit_listing', listing_id=listing_id)
                
        except ValueError:
            messages.error(request, "Please enter a valid price.")
            return redirect('edit_listing', listing_id=listing_id)
        
        # Update listing
        listing.title = title
        listing.description = description
        listing.price = price
        
        if category_id:
            listing.category = Category.objects.get(id=category_id)
        else:
            listing.category = None
            
        # Handle image updates based on the selected type
        if image_type == "file" and image_file:
            listing.imageFile = image_file
            listing.imageUrl = ""  # Clear URL when using file
        elif image_type == "url" and image_url:
            listing.imageUrl = image_url
            # Keep the existing file if any
            
        listing.save()
        
        messages.success(request, "Listing updated successfully!")
        return redirect('listing_detail', listing_id=listing_id)


@login_required
def close_listing(request, listing_id):
    """Close a listing (only by owner)"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if user is the owner
    if listing.owner != request.user:
        messages.error(request, "You can only close your own listings.")
        return redirect('listing_detail', listing_id=listing_id)
    
    if request.method == 'POST':
        listing.isActive = False
        listing.save()
        
        messages.success(request, f"'{listing.title}' has been closed successfully!")
        return redirect('listing_detail', listing_id=listing_id)
    
    # If GET request, redirect back to listing
    return redirect('listing_detail', listing_id=listing_id)
