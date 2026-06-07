from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    is_admin = db.Column(db.Boolean, default=False)  # Admin role flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    prediction_count = db.Column(db.Integer, default=0)  # Track number of predictions
    
    # Relationships
    properties = db.relationship('Property', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def make_admin(self):
        """Promote user to admin role"""
        self.is_admin = True
        self.role = 'admin'
        db.session.commit()
    
    def revoke_admin(self):
        """Remove admin role from user"""
        self.is_admin = False
        self.role = 'user'
        db.session.commit()
    
    def toggle_active(self):
        """Toggle user active status"""
        self.is_active = not self.is_active
        db.session.commit()
    
    def increment_prediction_count(self):
        """Increment user's prediction count"""
        self.prediction_count += 1
        db.session.commit()
    
    def get_properties_count(self):
        """Get user's property count"""
        return Property.query.filter_by(user_id=self.id).count()
    
    def get_predictions_count(self):
        """Get user's prediction count"""
        return Prediction.query.filter_by(property_id=self.id).count()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'prediction_count': self.prediction_count
        }

class Property(db.Model):
    """Property model for storing property data"""
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Property details
    property_type = db.Column(db.String(50), nullable=False)
    floor_number = db.Column(db.Integer, default=1)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    living_area = db.Column(db.Float, nullable=False)
    lot_size = db.Column(db.Float, nullable=False)
    year_built = db.Column(db.Integer, nullable=False)
    condition_rating = db.Column(db.Integer, nullable=False)
    location_code = db.Column(db.String(10), nullable=False)
    garage_size = db.Column(db.Integer, default=0)
    construction_quality = db.Column(db.String(20), nullable=False)
    climate_zone = db.Column(db.String(20), nullable=False)
    neighborhood_score = db.Column(db.Float, nullable=False)
    walkability_score = db.Column(db.Float, nullable=False)
    proximity_to_main_road = db.Column(db.String(20), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert property to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'property_type': self.property_type,
            'floor_number': self.floor_number,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'living_area': self.living_area,
            'lot_size': self.lot_size,
            'year_built': self.year_built,
            'condition_rating': self.condition_rating,
            'location_code': self.location_code,
            'garage_size': self.garage_size,
            'construction_quality': self.construction_quality,
            'climate_zone': self.climate_zone,
            'neighborhood_score': self.neighborhood_score,
            'walkability_score': self.walkability_score,
            'proximity_to_main_road': self.proximity_to_main_road,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_ml_features(self):
        """Convert property to ML features dictionary"""
        return {
            'Property_Type': self.property_type,
            'Floor_Number': self.floor_number,
            'Bedrooms': self.bedrooms,
            'Living_Area': self.living_area,
            'Lot_Size': self.lot_size,
            'Year_Built': self.year_built,
            'Condition_Rating': self.condition_rating,
            'Location_Code': self.location_code,
            'Garage_Size': self.garage_size,
            'Bathrooms': self.bathrooms,
            'Construction_Quality': self.construction_quality,
            'Climate_Zone': self.climate_zone,
            'Neighborhood_Score': self.neighborhood_score,
            'Walkability_Score': self.walkability_score,
            'Proximity_To_Main_Road': self.proximity_to_main_road
        }

class Prediction(db.Model):
    """Prediction model for storing prediction results"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    
    # Prediction results
    predicted_price = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    price_per_sqft = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(20), nullable=False)
    
    # Model metrics
    rmse = db.Column(db.Float)
    mae = db.Column(db.Float)
    r2_score = db.Column(db.Float)
    mape = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'predicted_price': self.predicted_price,
            'confidence_score': self.confidence_score,
            'price_per_sqft': self.price_per_sqft,
            'model_version': self.model_version,
            'rmse': self.rmse,
            'mae': self.mae,
            'r2_score': self.r2_score,
            'mape': self.mape,
            'created_at': self.created_at.isoformat()
        }

class ModelMetrics(db.Model):
    """Model for storing ML model performance metrics"""
    __tablename__ = 'model_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    model_version = db.Column(db.String(20), unique=True, nullable=False)
    
    # Performance metrics
    rmse = db.Column(db.Float, nullable=False)
    mae = db.Column(db.Float, nullable=False)
    r2_score = db.Column(db.Float, nullable=False)
    mape = db.Column(db.Float, nullable=False)
    
    # Training details
    training_samples = db.Column(db.Integer, nullable=False)
    training_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert metrics to dictionary"""
        return {
            'id': self.id,
            'model_version': self.model_version,
            'rmse': self.rmse,
            'mae': self.mae,
            'r2_score': self.r2_score,
            'mape': self.mape,
            'training_samples': self.training_samples,
            'training_date': self.training_date.isoformat()
        }
