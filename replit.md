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
- **DATABASE_URL** - PostgreSQL connection string (auto-configured by Replit)
- **SECRET_KEY** - Flask secret key for session security
- **GOOGLE_OAUTH_CLIENT_ID** - Google OAuth client ID for user authentication
- **GOOGLE_OAUTH_CLIENT_SECRET** - Google OAuth client secret
- **PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE** - Database credentials (auto-configured)

## Google OAuth Setup
To enable Google Sign-In:
1. Go to https://console.cloud.google.com/apis/credentials
2. Create or select an OAuth 2.0 Client ID
3. Add authorized redirect URI: `https://[your-replit-domain]/google_login/callback`
4. Copy Client ID and Client Secret to Replit Secrets

## Default Admin Credentials
- **Username**: admin
- **Password**: admin123
- ⚠️ **Important**: Change these credentials immediately after first login

## Recent Changes
- 2025-10-15: Major UI/UX Improvements and Google Authentication
  - **Visual Design Overhaul**: Completely redesigned CSS with modern, professional styling
    - New color scheme with better contrast and readability
    - Enhanced buttons with hover effects and smooth transitions
    - Improved form controls with better focus states
    - Responsive dropdown menus with custom styling
    - Modern card layouts with shadows and hover animations
  - **Google OAuth Integration**: Added Google Sign-In for users
    - Implemented Flask-Login for session management
    - Created User model in database for authenticated users
    - Added user login/registration with Google OAuth 2.0
    - User menu in navigation with avatar and logout functionality
    - Separate admin and user authentication systems
  - **Production-Ready Features**:
    - Proper error handling and flash messages
    - Secure session management
    - Environment variable configuration for all secrets
    - Database schema with User table
    - Improved navigation with user state awareness
  
- 2025-10-15: Initial setup for Replit environment
  - Configured Flask app to run on 0.0.0.0:5000
  - Integrated with Replit PostgreSQL database
  - Installed all Python dependencies (Flask, SQLAlchemy, Flask-Login, etc.)
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
