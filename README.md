# 🌍 **Booking System**  
![Booking](https://img.shields.io/badge/Django-5.2.4-brightgreen) ![DRF](https://img.shields.io/badge/DRF-API-red) ![MySQL](https://img.shields.io/badge/DB-MySQL-blue)


A web application for managing real estate listings, bookings, and reviews.  
Built with Django REST Framework.

---

## **Table of Contents**
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Installation & Launch](#installation--launch)
4. [Project Structure](#project-structure)
5. [Main API Endpoints](#main-api-endpoints)

---

## **Features**

### 1. **Property Listings Management**
- 🏠 Create listings (title, description, address, price, number of rooms, property type).  
- ✏️ Edit and delete your own listings.  
- 🔄 Toggle listing status (active/inactive).

### 2. **Search and Filtering**
- 🔍 Search by keywords in the title and description.  
- Filtering options:
  - By price (min/max)
  - By city (location)
  - By number of rooms
  - By property type  
- Sorting options:
  - By price  
  - By date added  
  - By popularity (number of reviews)

### 3. **Authentication and Authorization**
- 👥 User registration and login.  
- Role-based access:
  - **Tenant**: view and book listings.  
  - **Landlord**: create, edit, and delete listings.  
- 🔐 JWT authentication (SimpleJWT).

### 4. **Bookings**
- 📅 Create bookings with specified start and end dates.  
- View active and completed bookings.  
- ❌ Cancel a booking before a certain date.  
- ✅ Booking confirmation/rejection by the landlord.

### 5. **Ratings and Reviews**
- ⭐ Leave a review and rating after a completed booking.  
- View all reviews related to a listing.  

---

## **Tech Stack**
- **Backend:** Django 4.2, Django REST Framework  
- **Authentication:** SimpleJWT  
- **Database:** MySQL  
- **Filtering & Search:** django-filter, SearchFilter, OrderingFilter  
- **Environment Variables:** django-environ  

---

## **Installation & Launch**
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Final_project_Booking_system
   ```

2. Create a virtual environment:  
   ```bash
    python -m venv .venv
    source .venv/bin/activate
   ```
3. Install dependencies: 
   ```bash
    pip install -r requirements.txt
    pip freeze > requirements.txt
   ```
4. Configure .env:
   ```bash
   ...
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3
   ...
   ```
5. Apply migrations:
   ```bash
   python manage.py makemigrations 
   python manage.py runserver
   ```
6. Run the server:
   ```bash
   python manage.py runserver
   ```

## **Project Structure**
   ```bash
      Final_project_Booking_system/
        config/               # Project settings (urls, settings)
        apps/
          announcements/      # Models, serializers, and viewsets for listings
          bookings/           # Booking models and business logic
          reviews/            # Models and API for reviews
          users/              # Custom user model
        manage.py
        .env
        .gitignore
        requirements.txt
        .venv

   ```
## **Main API Endpoints**  
#### Authentication:
- POST /api/users/register/ — user registration & token generation
- POST /api/users/token/refresh/ — refresh token

#### Announcements:
- GET /api/announcements/ — list of listings (search/filter/sort)
- POST /api/announcements/ — create a listing
- PATCH /api/announcements/{id}/toggle_status/ — change listing status

#### Bookings:
- POST /api/bookings/ — create a booking
- GET /api/bookings/ — list of bookings

#### Reviews:
- POST /api/reviews/ — leave a review
- GET /api/review/{id} — get reviews for a booking

