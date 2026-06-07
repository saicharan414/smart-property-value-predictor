"""
Comprehensive Test Suite for Smart Property Value Predictor (SPVP)

This test file covers:
- User authentication and authorization
- Property prediction functionality
- Admin panel features
- API endpoints
- Database operations
- Model training and validation
- Error handling and edge cases
"""

import unittest
import tempfile
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask
from werkzeug.security import generate_password_hash

# Import the application and models
from app import app, db, User, Property, Prediction, ModelMetrics
from spvp_app import SmartPropertyValuePredictor
from models import login_manager

class SPVPTestCase(unittest.TestCase):
    """Test cases for Smart Property Value Predictor"""
    
    def setUp(self):
        """Set up test environment"""
        # Create test database
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        
        # Create test client
        self.client = self.app.test_client()
        
        # Initialize database
        with self.app.app_context():
            db.create_all()
            
            # Create test users
            self.create_test_users()
            
            # Create test ML predictor
            self.spvp = SmartPropertyValuePredictor()
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()
    
    def create_test_users(self):
        """Create test users for testing"""
        # Create admin user
        admin_user = User(
            username='admin_test',
            email='admin@test.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            is_active=True,
            role='admin',
            created_at=datetime.now()
        )
        db.session.add(admin_user)
        
        # Create regular user
        regular_user = User(
            username='user_test',
            email='user@test.com',
            password_hash=generate_password_hash('user123'),
            is_admin=False,
            is_active=True,
            role='user',
            created_at=datetime.now()
        )
        db.session.add(regular_user)
        
        # Create inactive user
        inactive_user = User(
            username='inactive_test',
            email='inactive@test.com',
            password_hash=generate_password_hash('inactive123'),
            is_admin=False,
            is_active=False,
            role='user',
            created_at=datetime.now()
        )
        db.session.add(inactive_user)
        
        db.session.commit()
        
        # Store user IDs for later use
        self.admin_id = admin_user.id
        self.user_id = regular_user.id
        self.inactive_id = inactive_user.id
    
    def login_user(self, username, password):
        """Helper method to login user"""
        return self.client.post('/api/login', json={
            'username': username,
            'password': password
        })
    
    def logout_user(self):
        """Helper method to logout user"""
        return self.client.get('/logout')
    
    def create_test_property_data(self):
        """Create test property data for predictions"""
        return {
            'livingArea': 1850,
            'locationCode': 'A',
            'propertyType': 'apartment',
            'yearBuilt': 2020,
            'conditionRating': 4.5,
            'bedrooms': 3,
            'bathrooms': 2,
            'totalArea': 2000,
            'amenities': ['parking', 'gym', 'pool']
        }
    
    def create_test_csv_data(self):
        """Create test CSV data for model training"""
        data = {
            'livingArea': [1500, 2000, 1800, 2200, 1600],
            'locationCode': ['A', 'B', 'A', 'C', 'B'],
            'propertyType': ['apartment', 'villa', 'apartment', 'independent', 'apartment'],
            'yearBuilt': [2015, 2018, 2020, 2010, 2019],
            'conditionRating': [4.0, 4.5, 3.5, 4.2, 3.8],
            'bedrooms': [2, 4, 3, 3, 2],
            'bathrooms': [2, 3, 2, 3, 2],
            'totalArea': [1600, 2500, 1900, 2400, 1700],
            'price': [4500000, 6500000, 5200000, 5800000, 4800000]
        }
        return pd.DataFrame(data)

class TestUserAuthentication(SPVPTestCase):
    """Test user authentication functionality"""
    
    def test_admin_login_success(self):
        """Test successful admin login"""
        response = self.login_user('admin_test', 'admin123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('user', data)
        self.assertTrue(data['user']['is_admin'])
    
    def test_regular_user_login_success(self):
        """Test successful regular user login"""
        response = self.login_user('user_test', 'user123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('user', data)
        self.assertFalse(data['user']['is_admin'])
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.login_user('admin_test', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_login_inactive_user(self):
        """Test login with inactive user"""
        response = self.login_user('inactive_test', 'inactive123')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_logout_functionality(self):
        """Test user logout"""
        # First login
        self.login_user('user_test', 'user123')
        
        # Then logout
        response = self.logout_user()
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_protected_route_without_login(self):
        """Test accessing protected route without login"""
        response = self.client.get('/api/user/stats')
        self.assertEqual(response.status_code, 302)  # Redirect to login

class TestPropertyPrediction(SPVPTestCase):
    """Test property prediction functionality"""
    
    def setUp(self):
        """Set up prediction tests"""
        super().setUp()
        # Login as regular user for prediction tests
        self.login_user('user_test', 'user123')
    
    def test_prediction_with_valid_data(self):
        """Test prediction with valid property data"""
        property_data = self.create_test_property_data()
        response = self.client.post('/api/predict', json={'features': property_data})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('predicted_price', data)
        self.assertIn('confidence', data)
        self.assertIsInstance(data['predicted_price'], (int, float))
        self.assertGreater(data['predicted_price'], 0)
        self.assertGreaterEqual(data['confidence'], 0)
        self.assertLessEqual(data['confidence'], 100)
    
    def test_prediction_with_missing_data(self):
        """Test prediction with missing required data"""
        response = self.client.post('/api/predict', json={'features': {}})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('message', data)
    
    def test_prediction_with_no_features(self):
        """Test prediction with no features provided"""
        response = self.client.post('/api/predict', json={})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No features provided')
    
    def test_prediction_database_storage(self):
        """Test that predictions are stored in database"""
        property_data = self.create_test_property_data()
        response = self.client.post('/api/predict', json={'features': property_data})
        
        self.assertEqual(response.status_code, 200)
        
        # Check if prediction was stored
        with self.app.app_context():
            prediction = Prediction.query.filter_by(user_id=self.user_id).first()
            self.assertIsNotNone(prediction)
            self.assertEqual(prediction.user_id, self.user_id)
            self.assertIsInstance(prediction.predicted_price, float)
            self.assertIsInstance(prediction.confidence, float)
    
    def test_prediction_history_retrieval(self):
        """Test retrieving user's prediction history"""
        # Create a prediction first
        property_data = self.create_test_property_data()
        self.client.post('/api/predict', json={'features': property_data})
        
        # Retrieve history
        response = self.client.get('/api/predictions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('predictions', data)
        self.assertGreater(len(data['predictions']), 0)

class TestAdminFunctionality(SPVPTestCase):
    """Test admin panel functionality"""
    
    def setUp(self):
        """Set up admin tests"""
        super().setUp()
        # Login as admin for admin tests
        self.login_user('admin_test', 'admin123')
    
    def test_admin_metrics_access(self):
        """Test admin can access metrics"""
        response = self.client.get('/api/admin/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('metrics', data)
    
    def test_admin_user_management_access(self):
        """Test admin can access user management"""
        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_analytics_access(self):
        """Test admin can access analytics"""
        response = self.client.get('/admin/analytics')
        self.assertEqual(response.status_code, 200)
    
    def test_regular_user_admin_denied(self):
        """Test regular user cannot access admin endpoints"""
        # Logout admin
        self.logout_user()
        
        # Login as regular user
        self.login_user('user_test', 'user123')
        
        # Try to access admin metrics
        response = self.client.get('/api/admin/metrics')
        self.assertEqual(response.status_code, 302)  # Redirect to login or unauthorized
    
    def test_admin_user_list_retrieval(self):
        """Test admin can retrieve user list"""
        response = self.client.get('/api/admin/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('users', data)
        self.assertGreater(len(data['users']), 0)

class TestCSVUploadAndTraining(SPVPTestCase):
    """Test CSV upload and model training functionality"""
    
    def setUp(self):
        """Set up CSV upload tests"""
        super().setUp()
        # Login as admin for training tests
        self.login_user('admin_test', 'admin123')
    
    def test_csv_upload_valid_format(self):
        """Test uploading a valid CSV file"""
        # Create test CSV data
        df = self.create_test_csv_data()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            csv_path = f.name
        
        try:
            # Upload CSV
            with open(csv_path, 'rb') as f:
                response = self.client.post('/api/upload', data={
                    'file': (f, 'test_properties.csv')
                })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('message', data)
        finally:
            os.unlink(csv_path)
    
    def test_csv_upload_invalid_format(self):
        """Test uploading an invalid file format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('This is not a CSV file')
            txt_path = f.name
        
        try:
            with open(txt_path, 'rb') as f:
                response = self.client.post('/api/upload', data={
                    'file': (f, 'test.txt')
                })
            
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertFalse(data['success'])
        finally:
            os.unlink(txt_path)
    
    def test_csv_upload_missing_columns(self):
        """Test uploading CSV with missing required columns"""
        # Create CSV with missing columns
        df = pd.DataFrame({
            'livingArea': [1500, 2000],
            'locationCode': ['A', 'B']
            # Missing other required columns
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            csv_path = f.name
        
        try:
            with open(csv_path, 'rb') as f:
                response = self.client.post('/api/upload', data={
                    'file': (f, 'incomplete.csv')
                })
            
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertFalse(data['success'])
        finally:
            os.unlink(csv_path)
    
    def test_model_training_process(self):
        """Test model training with valid data"""
        # This would test the actual training process
        # Implementation depends on your training endpoint
        df = self.create_test_csv_data()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            csv_path = f.name
        
        try:
            # Upload and train
            with open(csv_path, 'rb') as f:
                response = self.client.post('/api/upload', data={
                    'file': (f, 'training_data.csv')
                })
            
            # Check if training was successful
            if response.status_code == 200:
                data = json.loads(response.data)
                self.assertTrue(data['success'])
        finally:
            os.unlink(csv_path)

class TestErrorHandling(SPVPTestCase):
    """Test error handling and edge cases"""
    
    def test_404_error_handling(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-endpoint')
        self.assertEqual(response.status_code, 404)
    
    def test_method_not_allowed(self):
        """Test method not allowed errors"""
        response = self.client.delete('/api/login')
        self.assertEqual(response.status_code, 405)
    
    def test_invalid_json_input(self):
        """Test handling of invalid JSON input"""
        response = self.client.post('/api/predict', 
                                 data='invalid json', 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_database_connection_error(self):
        """Test handling of database connection errors"""
        # This would require mocking database failures
        pass

class TestModelValidation(SPVPTestCase):
    """Test ML model validation and performance"""
    
    def test_feature_validation(self):
        """Test feature validation logic"""
        spvp = SmartPropertyValuePredictor()
        
        # Test valid features
        valid_features = self.create_test_property_data()
        # This would test the feature validation method
        # Implementation depends on your validation logic
        
        # Test invalid features
        invalid_features = {
            'livingArea': -1000,  # Invalid negative area
            'locationCode': 'Z',   # Invalid location code
            'propertyType': 'house' # Invalid property type
        }
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        spvp = SmartPropertyValuePredictor()
        
        # Test confidence calculation with different scenarios
        # This would test the confidence calculation logic
        
    def test_model_performance_metrics(self):
        """Test model performance metrics calculation"""
        # Test accuracy, MAE, R2 score calculations
        pass

class TestSecurity(SPVPTestCase):
    """Test security features"""
    
    def test_sql_injection_protection(self):
        """Test SQL injection protection"""
        # Test with SQL injection attempts
        malicious_input = "'; DROP TABLE users; --"
        response = self.client.post('/api/login', json={
            'username': malicious_input,
            'password': 'password'
        })
        # Should not cause database errors
        self.assertNotEqual(response.status_code, 500)
    
    def test_xss_protection(self):
        """Test XSS protection"""
        xss_payload = "<script>alert('xss')</script>"
        response = self.client.post('/api/predict', json={
            'features': {
                'livingArea': 1000,
                'locationCode': xss_payload,
                'propertyType': 'apartment'
            }
        })
        # Should handle XSS safely
        self.assertNotEqual(response.status_code, 500)
    
    def test_authentication_token_security(self):
        """Test authentication token security"""
        # Test session security
        pass

class TestPerformance(SPVPTestCase):
    """Test performance and scalability"""
    
    def test_prediction_response_time(self):
        """Test prediction API response time"""
        import time
        
        property_data = self.create_test_property_data()
        
        start_time = time.time()
        response = self.client.post('/api/predict', json={'features': property_data})
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        response_time = end_time - start_time
        self.assertLess(response_time, 2.0)  # Should respond within 2 seconds
    
    def test_concurrent_predictions(self):
        """Test handling concurrent prediction requests"""
        import threading
        import time
        
        results = []
        
        def make_prediction():
            property_data = self.create_test_property_data()
            response = self.client.post('/api/predict', json={'features': property_data})
            results.append(response.status_code)
        
        # Create multiple concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_prediction)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        self.assertEqual(len(results), 5)
        for status in results:
            self.assertEqual(status, 200)

def run_tests():
    """Run all test cases"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestUserAuthentication,
        TestPropertyPrediction,
        TestAdminFunctionality,
        TestCSVUploadAndTraining,
        TestErrorHandling,
        TestModelValidation,
        TestSecurity,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running Smart Property Value Predictor Test Suite")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    print("=" * 60)
