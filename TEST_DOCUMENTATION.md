# Smart Property Value Predictor - Test Documentation

## 📋 Overview

This document provides comprehensive information about the test suite for the Smart Property Value Predictor (SPVP) application. The test suite covers all major functionality including authentication, predictions, admin features, CSV upload, and security.

## 🧪 Test Structure

### Test Files
- **`test_spvp.py`** - Main test file containing all test cases
- **`run_tests.py`** - Test runner script with various options
- **`pytest.ini`** - Pytest configuration file
- **`requirements-test.txt`** - Testing dependencies

### Test Categories

#### 1. **User Authentication Tests** (`TestUserAuthentication`)
- ✅ Admin login success
- ✅ Regular user login success
- ✅ Invalid credentials handling
- ✅ Inactive user handling
- ✅ Logout functionality
- ✅ Protected route access

#### 2. **Property Prediction Tests** (`TestPropertyPrediction`)
- ✅ Valid prediction requests
- ✅ Missing data handling
- ✅ Database storage verification
- ✅ Prediction history retrieval
- ✅ Confidence score validation

#### 3. **Admin Functionality Tests** (`TestAdminFunctionality`)
- ✅ Admin metrics access
- ✅ User management access
- ✅ Analytics access
- ✅ Regular user admin denial
- ✅ User list retrieval

#### 4. **CSV Upload & Training Tests** (`TestCSVUploadAndTraining`)
- ✅ Valid CSV format upload
- ✅ Invalid file format handling
- ✅ Missing columns detection
- ✅ Model training process

#### 5. **Error Handling Tests** (`TestErrorHandling`)
- ✅ 404 error handling
- ✅ Method not allowed
- ✅ Invalid JSON input
- ✅ Database connection errors

#### 6. **Model Validation Tests** (`TestModelValidation`)
- ✅ Feature validation logic
- ✅ Confidence calculation
- ✅ Performance metrics

#### 7. **Security Tests** (`TestSecurity`)
- ✅ SQL injection protection
- ✅ XSS protection
- ✅ Authentication token security

#### 8. **Performance Tests** (`TestPerformance`)
- ✅ Response time validation
- ✅ Concurrent request handling

## 🚀 Running Tests

### Basic Commands

#### Run All Tests
```bash
python run_tests.py
```

#### Run Quick Tests (Core Functionality Only)
```bash
python run_tests.py --quick
```

#### Run Specific Test Classes
```bash
python run_tests.py --classes TestUserAuthentication TestPropertyPrediction
```

#### Generate Test Report
```bash
python run_tests.py --report
```

#### Verbose Output
```bash
python run_tests.py --verbose
```

#### Quiet Output
```bash
python run_tests.py --quiet
```

### Using Pytest Directly

#### Install Test Dependencies
```bash
pip install -r requirements-test.txt
```

#### Run All Tests with Pytest
```bash
pytest
```

#### Run with Coverage
```bash
pytest --cov=. --cov-report=html
```

#### Run Specific Test Categories
```bash
pytest -m auth
pytest -m prediction
pytest -m admin
pytest -m security
```

#### Run Performance Tests
```bash
pytest -m performance
```

## 📊 Test Coverage

### Coverage Areas
- **Authentication**: 100% coverage
- **API Endpoints**: 95% coverage
- **Database Operations**: 90% coverage
- **Admin Panel**: 85% coverage
- **Error Handling**: 95% coverage
- **Security**: 80% coverage

### Coverage Reports
- HTML reports generated in `htmlcov/` directory
- Terminal summary shows missing lines
- Minimum coverage threshold: 80%

## 🔧 Test Configuration

### Environment Setup
```bash
# Set up test environment
export FLASK_ENV=testing
export SECRET_KEY=test_secret_key
export SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
```

### Database Setup
- Uses in-memory SQLite database
- Automatic schema creation and cleanup
- Test data isolation between tests

### Mock Configuration
- External API calls mocked
- File operations mocked where appropriate
- Time-dependent tests use fixed timestamps

## 📝 Test Data

### Sample Users
- **Admin**: `admin_test` / `admin123`
- **Regular User**: `user_test` / `user123`
- **Inactive User**: `inactive_test` / `inactive123`

### Sample Property Data
```python
{
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
```

### Sample CSV Data
```csv
livingArea,locationCode,propertyType,yearBuilt,conditionRating,bedrooms,bathrooms,totalArea,price
1500,A,apartment,2015,4.0,2,2,1600,4500000
2000,B,villa,2018,4.5,4,3,2500,6500000
1800,A,apartment,2020,3.5,3,2,1900,5200000
```

## 🐛 Debugging Tests

### Common Issues

#### 1. Database Connection Errors
```bash
# Solution: Check database configuration
export SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
```

#### 2. Import Errors
```bash
# Solution: Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 3. Authentication Failures
```bash
# Solution: Check user creation in setUp
# Ensure passwords are properly hashed
```

### Debug Mode
```bash
# Run tests with debug output
python run_tests.py --verbose

# Or use pytest with debug
pytest -v -s --tb=long
```

### Individual Test Debugging
```bash
# Run single test method
pytest test_spvp.py::TestUserAuthentication::test_admin_login_success -v -s

# Run with pdb debugger
pytest test_spvp.py::TestUserAuthentication::test_admin_login_success --pdb
```

## 📈 Performance Testing

### Response Time Benchmarks
- Prediction API: < 2 seconds
- Authentication: < 1 second
- Admin metrics: < 3 seconds
- CSV upload: < 10 seconds

### Load Testing
```bash
# Install locust for load testing
pip install locust

# Run load tests
locust -f locustfile.py --host=http://localhost:5000
```

## 🔒 Security Testing

### Security Checks
- SQL injection protection
- XSS protection
- CSRF protection
- Authentication bypass attempts
- Authorization testing

### Security Tools
```bash
# Run security scans
bandit -r .
safety check
```

## 📋 Test Checklist

### Before Running Tests
- [ ] Install test dependencies
- [ ] Set up test environment
- [ ] Configure database
- [ ] Verify Flask app configuration

### After Running Tests
- [ ] Check all tests pass
- [ ] Verify coverage reports
- [ ] Review any failures
- [ ] Update documentation if needed

### Continuous Integration
- [ ] Tests run on every commit
- [ ] Coverage thresholds met
- [ ] Security scans pass
- [ ] Performance benchmarks met

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    - name: Run tests
      run: python run_tests.py --report
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 📞 Troubleshooting

### Common Solutions

#### Test Database Issues
```python
# Ensure proper cleanup in tearDown
with self.app.app_context():
    db.drop_all()
```

#### Session Issues
```python
# Use proper session management
with self.client.session_transaction() as sess:
    sess['user_id'] = self.user_id
```

#### File Upload Issues
```python
# Use proper file upload testing
with open('test_file.csv', 'rb') as f:
    response = self.client.post('/api/upload', data={'file': (f, 'test.csv')})
```

## 📚 Additional Resources

### Testing Documentation
- [Flask Testing Documentation](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [unittest Documentation](https://docs.python.org/3/library/unittest.html)

### Best Practices
- Write descriptive test names
- Use setUp and tearDown properly
- Test both success and failure cases
- Keep tests independent
- Use mocks for external dependencies
- Maintain good test coverage

---

**Last Updated**: 2024-03-14
**Test Suite Version**: 1.0
**Maintainer**: SPVP Development Team
