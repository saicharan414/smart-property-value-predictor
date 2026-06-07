from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from models import User

class LoginForm(FlaskForm):
    """Login form for user authentication"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])

class RegistrationForm(FlaskForm):
    """Registration form for new users"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_username(self, username):
        """Validate username uniqueness"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Validate email uniqueness"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class PropertyForm(FlaskForm):
    """Property form for property data input"""
    property_type = SelectField('Property Type', choices=[
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('independent', 'Independent House')
    ], validators=[DataRequired()])
    
    floor_number = IntegerField('Floor Number', validators=[
        NumberRange(min=1, max=50, message='Floor number must be between 1 and 50')
    ], default=1)
    
    bedrooms = IntegerField('Bedrooms', validators=[
        NumberRange(min=1, max=20, message='Bedrooms must be between 1 and 20')
    ], default=3)
    
    bathrooms = IntegerField('Bathrooms', validators=[
        NumberRange(min=1, max=20, message='Bathrooms must be between 1 and 20')
    ], default=2)
    
    living_area = FloatField('Living Area (sq.ft)', validators=[
        NumberRange(min=100, max=50000, message='Living area must be between 100 and 50000 sq.ft')
    ], default=1850)
    
    lot_size = FloatField('Lot Size (sq.ft)', validators=[
        NumberRange(min=500, max=100000, message='Lot size must be between 500 and 100000 sq.ft')
    ], default=8000)
    
    year_built = IntegerField('Year Built', validators=[
        NumberRange(min=1900, max=2024, message='Year built must be between 1900 and 2024')
    ], default=2020)
    
    condition_rating = SelectField('Condition Rating', choices=[
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    ], coerce=int, validators=[DataRequired()])
    
    location_code = SelectField('Location Quality', choices=[
        ('A', 'A - Prime Location'),
        ('B', 'B - Good Location'),
        ('C', 'C - Average Location'),
        ('D', 'D - Developing Location')
    ], validators=[DataRequired()])
    
    garage_size = IntegerField('Garage Size', validators=[
        NumberRange(min=0, max=10, message='Garage size must be between 0 and 10')
    ], default=1)
    
    construction_quality = SelectField('Construction Quality', choices=[
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('good', 'Good'),
        ('premium', 'Premium')
    ], validators=[DataRequired()])
    
    climate_zone = SelectField('Climate Zone', choices=[
        ('tropical', 'Tropical'),
        ('moderate', 'Moderate'),
        ('cold', 'Cold'),
        ('arid', 'Arid')
    ], validators=[DataRequired()])
    
    neighborhood_score = FloatField('Neighborhood Score', validators=[
        NumberRange(min=1, max=10, message='Neighborhood score must be between 1 and 10')
    ], default=8.0)
    
    walkability_score = FloatField('Walkability Score', validators=[
        NumberRange(min=1, max=10, message='Walkability score must be between 1 and 10')
    ], default=8.5)
    
    proximity_to_main_road = SelectField('Proximity to Main Road', choices=[
        ('very_close', 'Very Close'),
        ('close', 'Close'),
        ('moderate', 'Moderate'),
        ('far', 'Far')
    ], validators=[DataRequired()])

class ProfileForm(FlaskForm):
    """Profile form for user profile management"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    
    def validate_email(self, email):
        """Validate email uniqueness (excluding current user)"""
        from flask_login import current_user
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Email already registered. Please use a different email.')
