-- Artist Portfolio Database Schema
-- PostgreSQL Database Schema for Artist Portfolio Application

-- Create database (run this manually in PostgreSQL)
-- CREATE DATABASE artist_portfolio;
-- \c artist_portfolio;

-- Enable UUID extension for generating unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Admin table for authentication
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Paintings table
CREATE TABLE painting (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL CHECK (category IN ('Abstract', 'Landscape', 'Portrait', 'Drawings', 'Semi-abstract')),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    size VARCHAR(100),
    medium VARCHAR(100),
    year INTEGER CHECK (year > 1900 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    image_url VARCHAR(500),
    available BOOLEAN DEFAULT TRUE,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exhibitions table
CREATE TABLE exhibition (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    venue VARCHAR(200),
    date VARCHAR(100),
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE "order" (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(100) UNIQUE NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    customer_email VARCHAR(200) NOT NULL,
    customer_phone VARCHAR(50),
    shipping_address TEXT,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES "order"(id) ON DELETE CASCADE,
    painting_id INTEGER REFERENCES painting(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1 CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact messages table
CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    subject VARCHAR(300),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'new' CHECK (status IN ('new', 'read', 'replied', 'archived')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_painting_category ON painting(category);
CREATE INDEX idx_painting_price ON painting(price);
CREATE INDEX idx_painting_available ON painting(available);
CREATE INDEX idx_painting_featured ON painting(featured);
CREATE INDEX idx_painting_created_at ON painting(created_at);

CREATE INDEX idx_order_status ON "order"(status);
CREATE INDEX idx_order_created_at ON "order"(created_at);
CREATE INDEX idx_order_customer_email ON "order"(customer_email);

CREATE INDEX idx_contact_status ON contact(status);
CREATE INDEX idx_contact_created_at ON contact(created_at);

CREATE INDEX idx_exhibition_created_at ON exhibition(created_at);

-- Create trigger to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_painting_updated_at BEFORE UPDATE ON painting
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_order_updated_at BEFORE UPDATE ON "order"
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO admin (username, email, password_hash) VALUES 
('admin', 'admin@artistportfolio.com', 'scrypt:32768:8:1$XvLj2qKuWJF5cTzw$4a8c89f1b2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0p1');

INSERT INTO painting (title, description, category, price, size, medium, year, image_url, featured, available) VALUES 
('Ethereal Landscapes', 'A mesmerizing abstract piece that captures the essence of natural landscapes through bold colors and fluid forms.', 'Abstract', 1500.00, '24x36 inches', 'Oil on Canvas', 2024, 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop', TRUE, TRUE),
('Mountain Solitude', 'Serene mountain landscape painted with oil on canvas, capturing the tranquil beauty of remote wilderness.', 'Landscape', 2200.00, '30x40 inches', 'Oil on Canvas', 2024, 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=800&h=600&fit=crop', TRUE, TRUE),
('Portrait in Blue', 'Intimate portrait study exploring human emotion through subtle color variations and expressive brushwork.', 'Portrait', 1800.00, '20x24 inches', 'Acrylic on Canvas', 2023, 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop', TRUE, TRUE),
('Urban Dreams', 'Contemporary semi-abstract interpretation of city life with mixed media techniques.', 'Semi-abstract', 1300.00, '18x24 inches', 'Mixed Media', 2023, 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop', FALSE, TRUE),
('Botanical Study', 'Detailed botanical drawing showcasing intricate natural forms and textures.', 'Drawings', 800.00, '12x16 inches', 'Charcoal on Paper', 2023, 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=800&h=600&fit=crop', FALSE, TRUE),
('Ocean Waves', 'Dynamic abstract representation of ocean movement through flowing brushstrokes and vibrant blues.', 'Abstract', 1700.00, '36x48 inches', 'Acrylic on Canvas', 2024, 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop', TRUE, TRUE);

INSERT INTO exhibition (title, venue, date, description, image_url) VALUES 
('Contemporary Visions', 'Modern Art Gallery', 'March 2024', 'Solo exhibition featuring 25 contemporary works exploring themes of nature and humanity.', 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=600&h=400&fit=crop'),
('Abstract Expressions', 'City Arts Center', 'September 2023', 'Group exhibition showcasing abstract works by emerging artists.', 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600&h=400&fit=crop'),
('Landscapes Reimagined', 'Heritage Museum', 'June 2023', 'Collaborative exhibition exploring traditional and contemporary landscape painting.', 'https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=600&h=400&fit=crop');

-- Create views for common queries
CREATE VIEW painting_summary AS
SELECT 
    category,
    COUNT(*) as total_paintings,
    AVG(price) as average_price,
    MIN(price) as min_price,
    MAX(price) as max_price,
    COUNT(CASE WHEN available = TRUE THEN 1 END) as available_paintings
FROM painting 
GROUP BY category;

CREATE VIEW order_summary AS
SELECT 
    DATE(created_at) as order_date,
    COUNT(*) as total_orders,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as average_order_value
FROM "order" 
GROUP BY DATE(created_at)
ORDER BY order_date DESC;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
