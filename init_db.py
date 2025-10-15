#!/usr/bin/env python3
"""
Database initialization script for Artist Portfolio Application
This script creates the database tables and populates them with sample data
"""
from dotenv import load_dotenv
load_dotenv()
from app import app, db, Painting, Exhibition, Contact, Admin, Order, OrderItem
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and sample data"""
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@artistportfolio.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Add sample paintings
        print("Adding sample paintings...")
        sample_paintings = [
            {
                'title': 'Ethereal Landscapes',
                'description': 'A mesmerizing abstract piece that captures the essence of natural landscapes through bold colors and fluid forms.',
                'category': 'Abstract',
                'price': 1500.00,
                'size': '24x36 inches',
                'medium': 'Oil on Canvas',
                'year': 2024,
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop',
                'featured': True,
                'available': True
            },
            {
                'title': 'Mountain Solitude',
                'description': 'Serene mountain landscape painted with oil on canvas, capturing the tranquil beauty of remote wilderness.',
                'category': 'Landscape',
                'price': 2200.00,
                'size': '30x40 inches',
                'medium': 'Oil on Canvas',
                'year': 2024,
                'image_url': 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=800&h=600&fit=crop',
                'featured': True,
                'available': True
            },
            {
                'title': 'Portrait in Blue',
                'description': 'Intimate portrait study exploring human emotion through subtle color variations and expressive brushwork.',
                'category': 'Portrait',
                'price': 1800.00,
                'size': '20x24 inches',
                'medium': 'Acrylic on Canvas',
                'year': 2023,
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop',
                'featured': True,
                'available': True
            },
            {
                'title': 'Urban Dreams',
                'description': 'Contemporary semi-abstract interpretation of city life with mixed media techniques.',
                'category': 'Semi-abstract',
                'price': 1300.00,
                'size': '18x24 inches',
                'medium': 'Mixed Media',
                'year': 2023,
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop',
                'featured': False,
                'available': True
            },
            {
                'title': 'Botanical Study',
                'description': 'Detailed botanical drawing showcasing intricate natural forms and textures.',
                'category': 'Drawings',
                'price': 800.00,
                'size': '12x16 inches',
                'medium': 'Charcoal on Paper',
                'year': 2023,
                'image_url': 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=800&h=600&fit=crop',
                'featured': False,
                'available': True
            },
            {
                'title': 'Ocean Waves',
                'description': 'Dynamic abstract representation of ocean movement through flowing brushstrokes and vibrant blues.',
                'category': 'Abstract',
                'price': 1700.00,
                'size': '36x48 inches',
                'medium': 'Acrylic on Canvas',
                'year': 2024,
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop',
                'featured': True,
                'available': True
            }
        ]
        
        for painting_data in sample_paintings:
            existing = Painting.query.filter_by(title=painting_data['title']).first()
            if not existing:
                painting = Painting(**painting_data)
                db.session.add(painting)
        
        # Add sample exhibitions
        print("Adding sample exhibitions...")
        sample_exhibitions = [
            {
                'title': 'Contemporary Visions',
                'venue': 'Modern Art Gallery',
                'date': 'March 2024',
                'description': 'Solo exhibition featuring 25 contemporary works exploring themes of nature and humanity.',
                'image_url': 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=600&h=400&fit=crop'
            },
            {
                'title': 'Abstract Expressions',
                'venue': 'City Arts Center',
                'date': 'September 2023',
                'description': 'Group exhibition showcasing abstract works by emerging artists.',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600&h=400&fit=crop'
            },
            {
                'title': 'Landscapes Reimagined',
                'venue': 'Heritage Museum',
                'date': 'June 2023',
                'description': 'Collaborative exhibition exploring traditional and contemporary landscape painting.',
                'image_url': 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=600&h=400&fit=crop'
            }
        ]
        
        for exhibition_data in sample_exhibitions:
            existing = Exhibition.query.filter_by(title=exhibition_data['title']).first()
            if not existing:
                exhibition = Exhibition(**exhibition_data)
                db.session.add(exhibition)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")
        print("\nDefault admin credentials:")
        print("Username: admin")
        print("Password: admin123")
        print("\nPlease change these credentials after first login!")

if __name__ == '__main__':
    init_database()
