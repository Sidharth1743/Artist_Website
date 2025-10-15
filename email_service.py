"""
Email service for sending notifications
"""
import os
from flask import render_template
from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with the app"""
    mail.init_app(app)

def send_order_confirmation(order, customer_email):
    """Send order confirmation email to customer"""
    try:
        msg = Message(
            subject=f'Order Confirmation - {order.order_number}',
            recipients=[customer_email],
            sender=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))
        )
        
        msg.html = render_template('emails/order_confirmation.html', order=order)
        msg.body = render_template('emails/order_confirmation.txt', order=order)
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending order confirmation: {e}")
        return False

def send_order_notification_to_admin(order):
    """Send new order notification to admin"""
    try:
        admin_email = os.getenv('ADMIN_EMAIL', os.getenv('MAIL_USERNAME'))
        
        msg = Message(
            subject=f'New Order Received - {order.order_number}',
            recipients=[admin_email],
            sender=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))
        )
        
        msg.html = render_template('emails/admin_order_notification.html', order=order)
        msg.body = render_template('emails/admin_order_notification.txt', order=order)
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending admin notification: {e}")
        return False

def send_contact_notification(contact):
    """Send contact form notification to admin"""
    try:
        admin_email = os.getenv('ADMIN_EMAIL', os.getenv('MAIL_USERNAME'))
        
        msg = Message(
            subject=f'New Contact Message: {contact.subject}',
            recipients=[admin_email],
            sender=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))
        )
        
        msg.html = render_template('emails/contact_notification.html', contact=contact)
        msg.body = render_template('emails/contact_notification.txt', contact=contact)
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending contact notification: {e}")
        return False

def send_contact_confirmation(contact):
    """Send confirmation email to person who submitted contact form"""
    try:
        msg = Message(
            subject='Thank you for contacting us',
            recipients=[contact.email],
            sender=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))
        )
        
        msg.html = render_template('emails/contact_confirmation.html', contact=contact)
        msg.body = render_template('emails/contact_confirmation.txt', contact=contact)
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending contact confirmation: {e}")
        return False
