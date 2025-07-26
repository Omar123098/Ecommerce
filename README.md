# 🛒 Django Marketplace Platform

> My take on building a modern e-commerce marketplace while learning Django! This project helped me understand web development fundamentals, from user authentication to inventory management with quantity-based purchasing systems.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.4.1-purple.svg)](https://getbootstrap.com)

## 📋 What's Inside
- [About This Project](#about-this-project)
- [What I Built](#what-i-built)
- [Tech Stack](#tech-stack)
- [File Structure](#file-structure)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [API Routes](#api-routes)
- [Database Design](#database-design)
- [Want to Contribute?](#want-to-contribute)

## 🎯 About This Project

I built this marketplace platform as a learning project to get hands-on experience with Django and web development. It's a comprehensive e-commerce marketplace where users can create listings with inventory management, buy items with quantity selection, and manage their profiles across 10 different categories.

The project helped me understand:
- How Django's MVT (Model-View-Template) architecture works
- User authentication and session management
- Database relationships and migrations
- Inventory management with quantity tracking
- Frontend integration with Bootstrap
- File uploads and image handling

### What Makes It Cool

- **User Accounts**: Sign up, log in, and manage your profile
- **Inventory Management**: Create listings with quantity tracking
- **Smart Purchasing**: Buy multiple items with automatic inventory updates
- **Categories**: 10 organized categories for better browsing
- **Watchlist**: Save items you're interested in
- **Admin Panel**: Built-in Django admin for managing everything
- **Responsive Design**: Works on desktop and mobile

## 🚀 What I Built

### 🔐 User System
- Register new accounts and log in securely
- Personal profile pages with activity stats
- Session management that keeps you logged in
- Password security (Django handles the hashing!)

### 🏷️ Product Listings
- Create listings with titles, descriptions, and prices
- Set quantity available for each item
- Upload images for your items (learned about file handling!)
- Organize by categories (10 different categories available)
- Activate/deactivate listings

### 💰 Purchase Features
- Buy items with quantity selection (1 to available stock)
- Secure purchase transaction handling with inventory updates
- Track purchase history for buyers and sellers
- Automatic listing status updates when items run out of stock
- Real-time total price calculation

### 🏷️ Category System
- **Home & Garden** - Furniture, appliances, home decor
- **Electronics** - Phones, computers, gaming, tech gadgets
- **Fashion & Clothing** - Clothing, shoes, accessories
- **Food & Drinks** - Gourmet foods, beverages, specialty items
- **Sports & Outdoors** - Sports equipment, outdoor gear
- **Books & Media** - Books, movies, music, educational materials
- **Toys & Games** - Toys, board games, video games, collectibles
- **Health & Beauty** - Skincare, cosmetics, health supplements
- **Automotive** - Car parts, accessories, tools
- **Art & Collectibles** - Artwork, antiques, vintage items

### ❤️ Watchlist System
- Add items to your personal watchlist
- Quick access to items you're following
- Remove items when you're no longer interested

### 📊 Profile Dashboard
- See your purchase history with quantities
- View your sales activity and inventory sold
- Track your created listings and stock levels
- Manage your watchlist items
- Personal statistics and activity overview

## 🛠️ Tech Stack

### Backend Technologies
- **Python 3.13** - The main programming language
- **Django 5.2.4** - Web framework that made everything easier
- **SQLite** - Database (perfect for learning and development)
- **Pillow 11.3.0** - For handling image uploads

### Frontend & Styling
- **HTML5 & CSS3** - The foundation of web pages
- **Bootstrap 4.4.1** - Made the styling so much easier!
- **FontAwesome** - Cool icons throughout the site
- **JavaScript** - For interactive features and real-time calculations

### Django Features I Used
- **Django ORM** - No need to write SQL queries manually
- **Django Admin** - Built-in admin panel (super useful!)
- **Django Forms** - Handles form validation automatically
- **Django Messages** - User notifications and feedback
- **Custom Management Commands** - For data management and setup

## 📁 File Structure

```
commerce/
├── .venv/                          # Virtual environment
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── commerce/                       # Django project root
    ├── manage.py                   # Django management script
    ├── db.sqlite3                  # SQLite database (development)
    ├── media/                      # User-uploaded files
    ├── marketplace/                # Main application (renamed from auctions)
    │   ├── models.py               # Database models with quantity system
    │   ├── views.py                # Business logic for marketplace
    │   ├── urls.py                 # URL routing
    │   ├── admin.py                # Admin configuration
    │   ├── forms.py                # Form definitions
    │   ├── migrations/             # Database migrations
    │   ├── management/             # Custom management commands
    │   │   └── commands/           # Command scripts
    │   │       ├── create_categories.py     # Category setup
    │   │       └── clear_user_data.py       # Data cleanup
    │   ├── static/marketplace/     # Static assets
    │   │   └── styles.css          # Custom CSS
    │   └── templates/marketplace/  # HTML templates
    │       ├── layout.html         # Base template
    │       ├── index.html          # Homepage
    │       ├── profile.html        # User profile
    │       ├── listing_detail.html # Product details
    │       └── ...                 # Other templates
    └── commerce/                   # Django configuration
        ├── settings.py             # Application settings
        ├── urls.py                 # Root URL configuration
        └── wsgi.py                 # WSGI application
```

## 🚀 Getting Started

Want to run this project locally? Here's how to set it up:

### What You'll Need
- Python 3.13+ on your computer
- That's pretty much it!

### Setup Steps

1. **Download the project**
   ```bash
   git clone https://github.com/Omar123098/Ecommerce.git
   cd Ecommerce
   ```

2. **Create a virtual environment** (keeps dependencies organized)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   .venv\Scripts\activate
   
   # On Mac/Linux
   source .venv/bin/activate
   ```

4. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

5. **Go to the main project folder**
   ```bash
   cd commerce
   ```

6. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create default categories**
   ```bash
   python manage.py create_categories
   ```

8. **Create an admin user** (optional but recommended)
   ```bash
   python manage.py createsuperuser
   ```

9. **Start the server**
   ```bash
   python manage.py runserver
   ```

10. **Check it out!**
    - Main site: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

### 🧹 Maintenance Commands

The project includes custom management commands for easy maintenance:

```bash
# Create the 10 default categories
python manage.py create_categories

# Clear all user data while preserving categories (useful for development)
python manage.py clear_user_data --confirm
```

## 📖 How to Use

### For Regular Users

1. **Sign Up**: Create your account with a username and password
2. **Browse Items**: Check out what's available for purchase on the homepage
3. **Filter by Category**: Use the category dropdown to find specific types of items
4. **Create Listings**: Got something to sell? Create a listing with photos, descriptions, and set your inventory quantity
5. **Buy Items**: Found something you want? Select quantity and purchase instantly!
6. **Use Watchlist**: Save items you're interested in for later
7. **Check Your Profile**: See your purchase history, sales, and current inventory

### For Admins

If you created a superuser account, you can access the admin panel to:
- Manage all users and their accounts
- View and moderate listings with inventory tracking
- See all purchases and transaction history
- Manage the 10 product categories
- Monitor inventory levels and stock movements
- Track platform statistics and user activity

## �️ API Routes

### Main Pages & Features

| URL | What It Does | Need to Login? |
|-----|--------------|----------------|
| `/` | Homepage with all active listings | Nope |
| `/login/` | Log into your account | Nope |
| `/register/` | Create a new account | Nope |
| `/logout/` | Log out | Yes |
| `/create/` | Create a new listing | Yes |
| `/listing/<id>/` | View details of a specific item | Nope |
| `/profile/` | Your personal dashboard | Yes |
| `/watchlist/` | Items you're watching | Yes |
| `/my-purchases/` | Your purchase history | Yes |
| `/purchase/<id>/` | Purchase an item | Yes |
| `/add-watchlist/<id>/` | Add item to watchlist | Yes |
| `/remove-watchlist/<id>/` | Remove from watchlist | Yes |

### Form Validations

The site checks for:
- **Registration**: Username must be unique, valid email format
- **Listings**: All required fields filled, valid price format, quantity must be at least 1
- **Purchasing**: Must be logged in, can't buy your own items, requested quantity must not exceed available stock

## �️ Database Design

### Database Tables (Models in Django)

Here's how I structured the data:

#### User Table (Built into Django)
```
- ID (unique identifier)
- Username (must be unique)
- Email address
- Password (Django hashes this automatically)
- Join date
```

#### Category Table
```
- ID
- Category name (like "Electronics", "Books", etc.)
```

#### Listing Table
```
- ID
- Title of the item
- Description
- Price (per item)
- Quantity available
- Quantity sold
- Image upload
- Which category it belongs to
- Who created it (links to User)
- Is it still active?
- Is it sold out?
- When it was created
- When it was sold out
```

#### Purchase Table
```
- ID
- Which listing was purchased
- Who bought it (buyer)
- Who sold it (seller)
- Quantity purchased
- Price per item
- Total price (quantity × price per item)
- When the purchase was made
```

#### Category Table
```
- ID
- Category name (Home & Garden, Electronics, Fashion, etc.)
- Description of the category
```

#### Watchlist Table
```
- ID
- Which user is watching
- Which listing they're watching
- When they added it
```

### How They Connect
- Users can create many listings with inventory quantities
- Users can make many purchases (as buyers) with different quantities
- Users can have many sales (as sellers) tracking total quantities sold
- Listings can have multiple purchases until inventory runs out
- Users can watch many listings to track availability
- Each listing belongs to one category
- Purchase history tracks individual transactions with quantities

## 🤝 Want to Contribute?

This was a learning project, but I'd love to see what improvements others might suggest! If you want to contribute:

### How to Help

1. Fork this repo
2. Create a new branch for your feature
3. Make your changes
4. Test everything works
5. Submit a pull request with a description of what you added

### Ideas for Improvements

Some things that could make this even better:
- **Better Security**: Two-factor authentication, stronger password requirements
- **Performance**: Add caching, optimize database queries
- **UI/UX**: Make it look even better, add animations
- **New Features**: Email notifications, payment integration, real-time notifications, bulk discounts
- **Testing**: Add unit tests and integration tests
- **Mobile App**: Maybe a React Native or Flutter version?
- **Advanced Search**: Search by price range, location, condition, availability
- **Analytics**: Sales reports, inventory tracking, profit calculations

### Found a Bug?

If something's not working right, please let me know! Open an issue and include:
- What you were trying to do
- What actually happened
- Steps to reproduce the problem
- Your browser/OS info

##  🙏 Thanks & Resources

Huge thanks to these amazing tools that made this project possible:

- **[Django](https://djangoproject.com/)** - Seriously the best web framework for learning
- **[Bootstrap](https://getbootstrap.com/)** - Made my CSS life so much easier
- **[FontAwesome](https://fontawesome.com/)** - Icons that actually look good
- **[Pillow](https://pillow.readthedocs.io/)** - For handling all the image uploads

Also shoutout to the Django documentation and community - you guys rock! 🚀

###Video

▶ [Watch Demo Video](https://youtu.be/VIDEO_ID)
