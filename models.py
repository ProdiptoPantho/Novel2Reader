from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create an instance of SQLAlchemy
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    temp_links = db.relationship('TempLink', backref='user', lazy=True)

class TempLink(db.Model):
    """Model representing a temporary link."""
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expiration_date
