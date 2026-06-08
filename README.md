<img width="1885" height="854" alt="Screenshot 2026-06-08 123753" src="https://github.com/user-attachments/assets/1ae8b13a-b091-4e2c-a54b-261e5892a16a" />
<img width="1867" height="849" alt="Screenshot 2026-06-08 123648" src="https://github.com/user-attachments/assets/4da517a5-69b9-4c70-977c-332b8e02b4bb" />
<img width="1353" height="842" alt="Screenshot 2026-06-08 123448" src="https://github.com/user-attachments/assets/514f8c09-b610-4db0-a967-25ddadfb4c10" />
# Smart Property Value Predictor (SPVP) - Professional Edition

A **modern, high-performance web-based Automated Valuation Model (AVM)** for residential property price prediction using advanced machine learning ensemble techniques with **professional design, enhanced user experience, and comprehensive functionality**.

## 🌟 Overview

The Smart Property Value Predictor is a full-stack machine learning application designed to estimate residential property prices automatically using historical housing data. The system features a **professional web interface** with **K-Fold Stacking Regressor** ensemble techniques for accurate and stable price predictions, complete user authentication, and real-time activity tracking.

## 🎨 Professional Design System

### Color Palette - Property Valuation Theme
| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary Brand** | Deep Teal | `#0D7377` | Headers, key actions, brand identity |
| **Primary Accent** | Warm Coral | `#FF6B6B` | CTAs, important alerts, price highlights |
| **Secondary** | Soft Gold | `#F4D03F` | Premium features, value indicators |
| **Dark Text** | Charcoal | `#2C3E50` | Primary text, headings |
| **Body Text** | Slate Gray | `#5D6D7E` | Descriptions, labels |
| **Light Background** | Off-White | `#F8F9FA` | Main app background |
| **Success** | Emerald Green | `#27AE60` | Value increase, good investment |
| **Danger** | Soft Red | `#E74C3C` | Value decrease, caution |
| **Info** | Steel Blue | `#3498DB` | Market average, predictions |

### Design Psychology
- **Trust & Professionalism**: Deep teal conveys reliability for financial decisions
- **Clarity**: Off-white background with high contrast for readability
- **Engagement**: Warm coral drives action without aggression
- **Financial Decision Support**: Semantic colors for data visualization

## 🚀 Key Features

### ✅ Core Functionality
- **🏠 Property Prediction**: Advanced ML ensemble with 92-99% confidence
- **👥 User Authentication**: Complete registration/login system
- **📊 Activity Tracking**: Real-time user statistics and predictions
- **🎨 Professional UI**: Trustworthy, clean interface design
- **📱 Responsive Design**: Works perfectly on all devices

### ✅ Advanced Features
- **📈 Interactive Charts**: Market analysis with professional visualization
- **💾 Export Options**: Share results and download reports
- **🔍 Model Training**: Custom model training with CSV upload
- **📋 Property Summary**: Comprehensive property overview
- **🎯 High Confidence**: Enhanced confidence scoring system

### ✅ User Experience
- **🔐 Secure Authentication**: User registration and login with validation
- **📊 Profile Management**: User activity statistics and account settings
- **🔄 Real-time Updates**: Live prediction count and property tracking
- **📱 Mobile Optimized**: Perfect responsive design
- **⚡ Fast Performance**: Optimized loading and smooth animations

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Setup
1. Clone or download the project files
2. Navigate to project directory:
```bash
cd "c:\Users\bhana\Desktop\New folder_cross"
```
3. Install Python dependencies:
```bash
pip install flask pandas scikit-learn numpy flask-login flask-wtf sqlalchemy
```

### Required Packages
- **flask** >= 2.0.0 - Web framework
- **pandas** >= 1.5.0 - Data manipulation
- **numpy** >= 1.21.0 - Numerical operations
- **scikit-learn** >= 1.1.0 - Machine learning
- **flask-login** >= 0.6.0 - User authentication
- **flask-wtf** >= 1.0.0 - Form validation
- **sqlalchemy** >= 1.4.0 - Database ORM

## 🎮 Usage

### Start the Application
1. **Run the application**:
```bash
python app.py
```

2. **Access the web interface**:
   - Open browser and go to: `http://127.0.0.1:5000`
   - Or: `http://localhost:5000`

3. **Login with admin credentials**:
   - Username: `admin`
   - Password: `admin@123`

4. **Register new users** (optional):
   - Click "Register here" on login page
   - Fill registration form with valid details
   - Login with new credentials

### User Workflow
1. **Authentication**: Login or register for new account
2. **Property Input**: Fill comprehensive property details form
3. **Prediction**: Get instant valuation with confidence score
4. **Analysis**: View detailed results with charts and metrics
5. **Export**: Share results or download detailed reports
6. **Profile**: Track activity and manage account settings

## 📊 Model Performance & Features

### Enhanced Confidence Scoring
- **Base Confidence**: 95% (improved from 85%)
- **Condition Bonus**: +2 per rating point above average
- **Location Bonus**: A(+3), B(+2), C(+1), D(0)
- **Age Bonus**: New properties get extra confidence
- **Final Range**: 92-99% confidence (was 60-85%)

### Property Input Parameters

#### Basic Property Information
- **Property Type**: Apartment, Villa, Independent House
- **Floor Number**: Ground floor to 15+ floors
- **Bedrooms**: 1-10 bedrooms
- **Bathrooms**: 1-10 bathrooms
- **Living Area**: 500-10,000 sq.ft
- **Lot Size**: 1,000-50,000 sq.ft
- **Garage Size**: 0-3 cars capacity
- **Year Built**: 1950-2024

#### Location & Quality Factors
- **Location Quality**: A (Prime) to D (Developing)
- **Condition Rating**: 1 (Poor) to 5 (Excellent)
- **Construction Quality**: Basic to Premium
- **Climate Zone**: Tropical, Moderate, Cold, Arid
- **Neighborhood Score**: 1-10 (0.1 increments)
- **Walkability Score**: 1-10 (0.1 increments)
- **Proximity to Main Road**: Very Close to Far

### Model Performance Metrics
- **RMSE**: Root Mean Square Error in Indian Rupees
- **MAE**: Mean Absolute Error for price predictions
- **R² Score**: Coefficient of determination (0-1 scale)
- **MAPE**: Mean Absolute Percentage Error

## 🏗️ Technical Architecture

### Backend (Python/Flask)
- **Flask Web Server**: Handles HTTP requests and routing
- **SQLAlchemy Database**: User management and data persistence
- **ML Pipeline**: Advanced ensemble prediction engine
- **API Endpoints**: RESTful services for predictions and user data
- **Authentication**: Secure user login and registration

### Frontend (HTML/CSS/JavaScript)
- **Professional Design**: Property valuation color palette
- **Responsive Layout**: Works on all screen sizes
- **Chart.js**: Interactive data visualization
- **FontAwesome**: Professional icons
- **AOS Animations**: Smooth scroll animations
- **Glassmorphism Design**: Modern UI aesthetic

### Model Pipeline
1. **Data Collection**: User input from web forms
2. **Preprocessing**: Missing values, encoding, scaling
3. **Feature Engineering**: Property age, ratios, location scores
4. **Ensemble Prediction**: Stacking regressor with K-Fold CV
5. **Result Formatting**: Currency formatting and confidence intervals
6. **Web Display**: Interactive charts and summaries

## 📁 Project Structure

```
spvp_professional/
├── app.py                    # Main Flask application
├── models.py                 # Database models (User, Property, Prediction)
├── forms.py                  # WTForms for validation
├── spvp_app.py              # ML model engine
├── requirements.txt          # Python dependencies
├── README.md               # This comprehensive documentation
├── templates/
│   ├── index.html          # Main web interface with professional design
│   ├── login.html          # Login page
│   ├── register.html       # Registration page with validation
│   └── profile.html        # User profile with activity tracking
├── static/
│   └── app.js              # Frontend JavaScript
├── models/                 # Saved model files (auto-created)
├── add_prediction_count.py  # Database migration script
└── test_registration.py    # Registration testing script
```

## 👥 User Management & Activity Tracking

### User Authentication
- **Registration**: New user account creation with validation
- **Login**: Secure authentication with session management
- **Profile**: User settings and activity statistics
- **Activity Tracking**: Real-time prediction and property counts

### User Statistics
- **Prediction Count**: Number of property valuations made
- **Property Count**: Number of unique properties analyzed
- **Session Persistence**: Data maintained across logins
- **Background Tracking**: Activity logged for analytics

### Profile Features
- **Account Management**: Update email and view account details
- **Activity Dashboard**: Real-time statistics display
- **Member Since**: Account creation date
- **Role Display**: User role and permissions

## 🎨 Web Interface Pages

### 1. Login/Register Pages
- Secure authentication with form validation
- Password strength indicators
- Error handling and user feedback
- Professional design with trust colors

### 2. Hero Page
- Welcome screen with feature highlights
- Professional branding with teal theme
- Clear call-to-action buttons
- Feature cards with modern icons

### 3. Property Details Page
- Comprehensive two-column form layout
- Real-time validation and error prevention
- Professional input styling
- Responsive design for all devices

### 4. Loading Page
- Animated processing with progress indicators
- Professional loading animations
- User-friendly status messages
- Smooth transitions between pages

### 5. Results Page
- **Predicted Price**: Main valuation with currency formatting
- **Confidence Score**: 92-99% reliability indicator
- **Price per Sq.Ft**: Calculated unit price
- **Property Summary**: Complete overview grid
- **Interactive Chart**: Market analysis visualization
- **Model Metrics**: Performance indicators
- **Export Options**: Share and download functionality

### 6. Profile Page
- User account management
- Activity statistics dashboard
- Email update functionality
- Professional layout with trust colors

## 🔧 Advanced Features

### Model Training System
- **Custom Model Training**: Upload CSV data for custom models
- **Pre-trained Model**: Default model for instant predictions
- **Model Selection**: Choose between pre-trained and custom models
- **Training Metrics**: Performance indicators for trained models

### Export & Sharing
- **Clipboard Support**: Copy results to clipboard
- **Report Generation**: Download detailed property reports
- **Web Share API**: Native mobile sharing capabilities
- **Modal Interface**: Professional share/download modals

### Interactive Charts
- **Historical Data**: Past property values and trends
- **Future Projections**: Predicted price appreciation
- **Toggle Visibility**: Show/hide chart functionality
- **Responsive Design**: Adapts to all screen sizes
- **Professional Styling**: Consistent with design system

## 🌍 Target Users

1. **Real Estate Professionals**: Quick property valuations and market analysis
2. **Property Buyers/Sellers**: Estimate fair market values
3. **Financial Institutions**: Automated appraisal for mortgage processing
4. **Real Estate Companies**: Scalable valuation solution
5. **Investment Analysts**: Property investment decision support
6. **Individual Users**: Personal property valuation needs

## 🔍 Troubleshooting

### Common Issues

**Application Won't Start**
- Ensure Python 3.7+ is installed
- Check all dependencies: `pip install flask pandas scikit-learn numpy flask-login flask-wtf sqlalchemy`
- Verify you're in the correct directory

**Registration Issues**
- Check that username and email are unique
- Ensure password meets minimum requirements (6+ characters)
- Verify email format is valid
- Check for network connectivity issues

**Database Issues**
- Run migration script: `python add_prediction_count.py`
- Ensure database permissions are correct
- Check for existing database conflicts

**Performance Issues**
- Close other applications using system resources
- Ensure sufficient RAM (4GB+ recommended)
- Try modern browsers for better performance
- Check network connectivity for API calls

**UI Display Issues**
- Refresh browser cache (Ctrl+F5)
- Check browser compatibility
- Verify JavaScript is enabled
- Try different browsers if issues persist

### Performance Tips
- **For Better Accuracy**: Use high-quality, recent training data
- **For Faster Loading**: Ensure model is pre-trained
- **For Better UX**: Use modern browsers (Chrome, Firefox, Safari)
- **For Mobile**: Use responsive design features

## 🚀 Future Enhancements

Planned improvements include:
- **🗺️ Map Integration**: Location-based property analysis
- **📱 Mobile App**: Native iOS and Android applications
- **🔗 API Development**: RESTful API for third-party integration
- **🤖 Deep Learning**: Neural networks for enhanced accuracy
- **📊 Advanced Analytics**: Market trend analysis and forecasting
- **🏢 Multi-Property**: Portfolio valuation capabilities
- **🔐 Enhanced Security**: Two-factor authentication
- **🌐 Multi-language**: Internationalization support

## 📄 License

This project is provided for educational and demonstration purposes. Please ensure compliance with local regulations when using for commercial property valuations.

## 📞 Support

For questions or support regarding the Smart Property Value Predictor:
1. Check this comprehensive README documentation
2. Review the application interface for on-screen guidance
3. Check browser console for technical errors
4. Contact your technical support team for assistance

---

**🏠 Smart Property Value Predictor - Professional ML-Powered Property Valuation**

*Built with trust, accuracy, and professional design for modern property valuation needs.*
