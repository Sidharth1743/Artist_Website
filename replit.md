# Artist Portfolio Application

## Overview
A Flask-based web application for showcasing an artist's portfolio with paintings, exhibitions, and e-commerce functionality. The application includes a complete admin panel for managing content and orders.

## Project Structure
- **app.py** - Main Flask application with routes, models, and business logic
- **run.py** - Application entry point configured for Replit environment
- **init_db.py** - Database initialization script with sample data
- **config.py** - Configuration settings for different environments
- **templates/** - Jinja2 HTML templates for frontend
- **static/** - CSS, JavaScript, and uploaded images
- **database_schema.sql** - SQL schema documentation

## Technology Stack
- **Backend**: Python 3.11, Flask 3.1.2
- **Database**: PostgreSQL (Neon-backed)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Forms**: Flask-WTF with WTForms
- **Migrations**: Flask-Migrate with Alembic
- **Image Processing**: Pillow

## Database
The application uses Replit's built-in PostgreSQL database with the following tables:
- **admin** - Admin user authentication
- **painting** - Artwork catalog
- **exhibition** - Exhibition information
- **order** - Customer orders
- **order_item** - Order line items
- **contact** - Contact form submissions
- **cart** - Shopping cart items (session-based)
- **wishlist** - User wishlist items (session-based)

## Features
### Public Features
- Browse paintings by category and price range
- View detailed painting information
- Shopping cart with session management
- Wishlist functionality
- Checkout and order placement
- Contact form
- Exhibition gallery

### Admin Features
- Dashboard with statistics
- Manage paintings (CRUD operations)
- Manage exhibitions (CRUD operations)
- View and manage orders
- View contact submissions
- Image upload functionality

## Environment Variables
- **DATABASE_URL** - PostgreSQL connection string (auto-configured)
- **SECRET_KEY** - Flask secret key for session security
- **PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE** - Database credentials (auto-configured)

## Default Admin Credentials
- **Username**: admin
- **Password**: admin123
- ⚠️ **Important**: Change these credentials immediately after first login

## Recent Changes
- 2025-10-15: Initial setup for Replit environment
  - Configured Flask app to run on 0.0.0.0:5000
  - Integrated with Replit PostgreSQL database
  - Installed all Python dependencies
  - Initialized database with sample data
  - Created uploads directory for image storage

## Running the Application
The application runs automatically via the configured workflow. Access:
- **Main Site**: Available via the Replit webview
- **Admin Panel**: Navigate to `/admin` route

## Deployment
The application is configured for autoscale deployment on Replit. It will:
- Automatically scale based on traffic
- Use the production-ready configuration
- Connect to the PostgreSQL database automatically

## Key Routes
- `/` - Home page with featured artworks
- `/paintings` - Browse all paintings with filters
- `/painting/<id>` - Individual painting details
- `/gallery` - Exhibition gallery
- `/about` - About the artist
- `/contact` - Contact form
- `/cart` - Shopping cart
- `/wishlist` - User wishlist
- `/checkout` - Checkout process
- `/admin` - Admin login
- `/admin/dashboard` - Admin dashboard (requires login)
