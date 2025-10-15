from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models
class Painting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    size = db.Column(db.String(100))
    medium = db.Column(db.String(100))
    year = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    available = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': float(self.price),
            'size': self.size,
            'medium': self.medium,
            'year': self.year,
            'image_url': self.image_url,
            'available': self.available,
            'featured': self.featured
        }

class Exhibition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(200))
    date = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'venue': self.venue,
            'date': self.date,
            'description': self.description,
            'image_url': self.image_url
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(100), unique=True, nullable=False)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50))
    shipping_address = db.Column(db.Text)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    painting_id = db.Column(db.Integer, db.ForeignKey('painting.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    painting = db.relationship('Painting', backref='order_items')

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(300))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    painting_id = db.Column(db.Integer, db.ForeignKey('painting.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    painting = db.relationship('Painting', backref='cart_items')

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    painting_id = db.Column(db.Integer, db.ForeignKey('painting.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    painting = db.relationship('Painting', backref='wishlist_items')

# Forms
class PaintingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    category = SelectField('Category', choices=[
        ('Abstract', 'Abstract'),
        ('Landscape', 'Landscape'),
        ('Portrait', 'Portrait'),
        ('Drawings', 'Drawings'),
        ('Semi-abstract', 'Semi-abstract')
    ], validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    size = StringField('Size')
    medium = StringField('Medium')
    year = IntegerField('Year')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    featured = SelectField('Featured', choices=[('0', 'No'), ('1', 'Yes')], coerce=int)

class ExhibitionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    venue = StringField('Venue')
    date = StringField('Date')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject')
    message = TextAreaField('Message', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    featured_paintings = Painting.query.filter_by(featured=True).limit(6).all()
    return render_template('index.html', paintings=featured_paintings)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    exhibitions = Exhibition.query.order_by(Exhibition.created_at.desc()).all()
    return render_template('gallery.html', exhibitions=exhibitions)

@app.route('/paintings')
def paintings():
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = Painting.query.filter_by(available=True)
    
    if category:
        query = query.filter_by(category=category)
    if min_price is not None:
        query = query.filter(Painting.price >= min_price)
    if max_price is not None:
        query = query.filter(Painting.price <= max_price)
    
    paintings = query.order_by(Painting.created_at.desc()).all()
    categories = db.session.query(Painting.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('paintings.html', paintings=paintings, categories=categories)

@app.route('/painting/<int:id>')
def painting_detail(id):
    painting = Painting.query.get_or_404(id)
    return render_template('painting_detail.html', painting=painting)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

# API Routes
@app.route('/api/paintings')
def api_paintings():
    paintings = Painting.query.filter_by(available=True).all()
    return jsonify([painting.to_dict() for painting in paintings])

@app.route('/api/paintings/<int:id>')
def api_painting(id):
    painting = Painting.query.get_or_404(id)
    return jsonify(painting.to_dict())

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def api_cart():
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    
    if request.method == 'GET':
        # Get cart items
        cart_items = Cart.query.filter_by(session_id=session_id).all()
        items = []
        for item in cart_items:
            if item.painting:
                items.append({
                    'id': item.painting.id,
                    'title': item.painting.title,
                    'price': float(item.painting.price),
                    'imageUrl': item.painting.image_url,
                    'quantity': item.quantity
                })
        return jsonify(items)
    
    elif request.method == 'POST':
        # Add to cart
        data = request.get_json()
        painting_id = data.get('painting_id')
        quantity = data.get('quantity', 1)
        
        painting = Painting.query.get_or_404(painting_id)
        
        # Check if already in cart
        cart_item = Cart.query.filter_by(session_id=session_id, painting_id=painting_id).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(session_id=session_id, painting_id=painting_id, quantity=quantity)
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Added to cart',
            'painting': painting.to_dict()
        })
    
    elif request.method == 'DELETE':
        # Remove from cart
        painting_id = request.args.get('painting_id', type=int)
        if painting_id:
            Cart.query.filter_by(session_id=session_id, painting_id=painting_id).delete()
        else:
            # Clear entire cart
            Cart.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        return jsonify({'success': True})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    if 'session_id' not in session:
        return jsonify({'success': False, 'message': 'No session'})
    
    data = request.get_json()
    painting_id = data.get('painting_id')
    quantity = data.get('quantity', 1)
    
    cart_item = Cart.query.filter_by(session_id=session['session_id'], painting_id=painting_id).first()
    
    if cart_item:
        if quantity > 0:
            cart_item.quantity = quantity
        else:
            db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Item not found'})

@app.route('/api/wishlist', methods=['GET', 'POST', 'DELETE'])
def api_wishlist():
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    
    if request.method == 'GET':
        # Get wishlist items
        wishlist_items = Wishlist.query.filter_by(session_id=session_id).all()
        items = [item.painting_id for item in wishlist_items if item.painting]
        return jsonify(items)
    
    elif request.method == 'POST':
        # Add to wishlist
        data = request.get_json()
        painting_id = data.get('painting_id')
        
        painting = Painting.query.get_or_404(painting_id)
        
        # Check if already in wishlist
        wishlist_item = Wishlist.query.filter_by(session_id=session_id, painting_id=painting_id).first()
        
        if not wishlist_item:
            wishlist_item = Wishlist(session_id=session_id, painting_id=painting_id)
            db.session.add(wishlist_item)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Added to wishlist'
        })
    
    elif request.method == 'DELETE':
        # Remove from wishlist
        painting_id = request.args.get('painting_id', type=int)
        if painting_id:
            Wishlist.query.filter_by(session_id=session_id, painting_id=painting_id).delete()
            db.session.commit()
        return jsonify({'success': True})

@app.route('/cart')
def cart():
    # Sync localStorage to database on page load
    return render_template('cart.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        data = request.get_json()
        
        # Create order
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        order = Order(
            order_number=order_number,
            customer_name=data.get('name'),
            customer_email=data.get('email'),
            customer_phone=data.get('phone'),
            shipping_address=data.get('address'),
            total_amount=data.get('total'),
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order items
        for item in data.get('items', []):
            order_item = OrderItem(
                order_id=order.id,
                painting_id=item['id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_number': order_number,
            'message': 'Order placed successfully!'
        })
    
    return render_template('checkout.html')

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    paintings_count = Painting.query.count()
    orders_count = Order.query.count()
    exhibitions_count = Exhibition.query.count()
    contacts_count = Contact.query.filter_by(status='new').count()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         paintings_count=paintings_count,
                         orders_count=orders_count,
                         exhibitions_count=exhibitions_count,
                         contacts_count=contacts_count,
                         recent_orders=recent_orders)

@app.route('/admin/paintings')
@admin_required
def admin_paintings():
    paintings = Painting.query.order_by(Painting.created_at.desc()).all()
    return render_template('admin/paintings.html', paintings=paintings)

@app.route('/admin/paintings/add', methods=['GET', 'POST'])
@admin_required
def admin_add_painting():
    form = PaintingForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        painting = Painting(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            price=form.price.data,
            size=form.size.data,
            medium=form.medium.data,
            year=form.year.data,
            image_url=f"/static/uploads/{filename}" if filename else None,
            featured=bool(form.featured.data)
        )
        db.session.add(painting)
        db.session.commit()
        flash('Painting added successfully!', 'success')
        return redirect(url_for('admin_paintings'))
    
    return render_template('admin/add_painting.html', form=form)

@app.route('/admin/paintings/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_painting(id):
    painting = Painting.query.get_or_404(id)
    form = PaintingForm(obj=painting)
    
    if form.validate_on_submit():
        painting.title = form.title.data
        painting.description = form.description.data
        painting.category = form.category.data
        painting.price = form.price.data
        painting.size = form.size.data
        painting.medium = form.medium.data
        painting.year = form.year.data
        painting.featured = bool(form.featured.data)
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            painting.image_url = f"/static/uploads/{filename}"
        
        db.session.commit()
        flash('Painting updated successfully!', 'success')
        return redirect(url_for('admin_paintings'))
    
    return render_template('admin/edit_painting.html', form=form, painting=painting)

@app.route('/admin/paintings/delete/<int:id>')
@admin_required
def admin_delete_painting(id):
    painting = Painting.query.get_or_404(id)
    db.session.delete(painting)
    db.session.commit()
    flash('Painting deleted successfully!', 'success')
    return redirect(url_for('admin_paintings'))

@app.route('/admin/exhibitions')
@admin_required
def admin_exhibitions():
    exhibitions = Exhibition.query.order_by(Exhibition.created_at.desc()).all()
    return render_template('admin/exhibitions.html', exhibitions=exhibitions)

@app.route('/admin/exhibitions/add', methods=['GET', 'POST'])
@admin_required
def admin_add_exhibition():
    form = ExhibitionForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        exhibition = Exhibition(
            title=form.title.data,
            venue=form.venue.data,
            date=form.date.data,
            description=form.description.data,
            image_url=f"/static/uploads/{filename}" if filename else None
        )
        db.session.add(exhibition)
        db.session.commit()
        flash('Exhibition added successfully!', 'success')
        return redirect(url_for('admin_exhibitions'))
    
    return render_template('admin/add_exhibition.html', form=form)

@app.route('/admin/exhibitions/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_exhibition(id):
    exhibition = Exhibition.query.get_or_404(id)
    form = ExhibitionForm(obj=exhibition)
    
    if form.validate_on_submit():
        exhibition.title = form.title.data
        exhibition.venue = form.venue.data
        exhibition.date = form.date.data
        exhibition.description = form.description.data
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            exhibition.image_url = f"/static/uploads/{filename}"
        
        db.session.commit()
        flash('Exhibition updated successfully!', 'success')
        return redirect(url_for('admin_exhibitions'))
    
    return render_template('admin/edit_exhibition.html', form=form, exhibition=exhibition)

@app.route('/admin/exhibitions/delete/<int:id>')
@admin_required
def admin_delete_exhibition(id):
    exhibition = Exhibition.query.get_or_404(id)
    db.session.delete(exhibition)
    db.session.commit()
    flash('Exhibition deleted successfully!', 'success')
    return redirect(url_for('admin_exhibitions'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user if it doesn't exist
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)