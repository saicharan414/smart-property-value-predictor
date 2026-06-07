import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import RidgeCV, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

class SmartPropertyValuePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.target_column = "Sale_Price"
        self.model_metrics = {}
        
        # Default hyperparameters
        self.k_folds = 5
        self.rf_trees = 100
        self.gb_trees = 100
        self.learning_rate = 0.1
        self.knn_neighbors = 5
        
    def display_header(self):
        print("=" * 50)
        print("    Smart Property Value Predictor (SPVP)")
        print("=" * 50)
        print("Automated Valuation Model for Residential Properties")
        print("Using K-Fold Stacking Regressor")
        print("=" * 50)
        
    def display_main_menu(self):
        print("\nMAIN MENU")
        print("-" * 30)
        print("1. Upload Dataset")
        print("2. Train Model")
        print("3. Predict Property Price")
        print("4. View Model Metrics")
        print("5. Save/Load Model")
        print("6. Exit")
        print("-" * 30)
        
    def load_dataset(self):
        """Load and validate dataset"""
        print("\n" + "="*40)
        print("UPLOAD DATASET")
        print("="*40)
        
        while True:
            file_path = input("Enter dataset file path (or 'demo' for sample data): ").strip()
            
            if file_path.lower() == 'demo':
                return self.create_sample_dataset()
            
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found. Please try again.")
                continue
                
            try:
                data = pd.read_csv(file_path)
                print(f"\nDataset loaded successfully!")
                print(f"Shape: {data.shape}")
                print(f"Columns: {list(data.columns)}")
                
                # Check if target column exists
                if self.target_column not in data.columns:
                    print(f"Warning: Target column '{self.target_column}' not found.")
                    print("Available columns:", list(data.columns))
                    target = input("Enter target column name: ").strip()
                    if target in data.columns:
                        self.target_column = target
                    else:
                        print("Invalid target column. Using first numeric column as target.")
                        numeric_cols = data.select_dtypes(include=[np.number]).columns
                        self.target_column = numeric_cols[0] if len(numeric_cols) > 0 else data.columns[0]
                
                return data
                
            except Exception as e:
                print(f"Error loading dataset: {e}")
                continue
    
    def create_sample_dataset(self):
        """Create a sample housing dataset for demonstration"""
        print("\nCreating sample dataset...")
        
        np.random.seed(42)
        n_samples = 1000
        
        # Generate sample data with enhanced features based on Hyderabad market
        data = {
            'Property_Type': np.random.choice(['apartment', 'villa', 'independent'], n_samples, p=[0.6, 0.25, 0.15]),
            'Floor_Number': np.random.randint(1, 17, n_samples),  # 16 floors max
            'Bedrooms': np.random.randint(1, 6, n_samples),
            'Living_Area': np.random.normal(1850, 400, n_samples),  # Around 1850 sq.ft
            'Lot_Size': np.random.normal(8000, 2000, n_samples),
            'Year_Built': np.random.randint(2000, 2023, n_samples),  # Newer properties
            'Condition_Rating': np.random.randint(1, 6, n_samples),
            'Location_Code': np.random.choice(['A', 'B', 'C', 'D'], n_samples, p=[0.2, 0.3, 0.3, 0.2]),
            'Garage_Size': np.random.randint(0, 4, n_samples),
            'Bathrooms': np.random.randint(1, 5, n_samples),
            'Construction_Quality': np.random.choice(['premium', 'good', 'standard', 'basic'], n_samples, p=[0.2, 0.3, 0.4, 0.1]),
            'Climate_Zone': np.random.choice(['tropical', 'moderate', 'cold', 'arid'], n_samples, p=[0.4, 0.4, 0.1, 0.1]),
            'Neighborhood_Score': np.random.uniform(6, 10, n_samples),  # Better neighborhoods
            'Walkability_Score': np.random.uniform(7, 10, n_samples),  # Good walkability
            'Proximity_To_Main_Road': np.random.choice(['very_close', 'close', 'moderate', 'far'], n_samples, p=[0.3, 0.3, 0.2, 0.2])
        }
        
        df = pd.DataFrame(data)
        
        # Create realistic price based on Hyderabad market data (2025: ₹7,800 per sq.ft)
        base_price_per_sqft = 7800  # Hyderabad average 2025
        
        # Location multipliers based on Hyderabad areas
        location_multipliers = {
            'A': 1.4,  # Premium: Gachibowli, Kokapet (₹9,000-11,000 per sq.ft)
            'B': 1.1,  # Good: Kondapur, Bachupally (₹8,000-9,000 per sq.ft)
            'C': 0.9,  # Average: (₹7,000-8,000 per sq.ft)
            'D': 0.7   # Developing: (₹5,000-6,000 per sq.ft)
        }
        
        # Proximity to main road multipliers
        proximity_multipliers = {
            'very_close': 1.15,  # < 100m
            'close': 1.08,       # 100-500m
            'moderate': 1.0,     # 500m-1km
            'far': 0.92          # > 1km
        }
        
        # Property type multipliers
        property_type_multipliers = {
            'apartment': 1.0,
            'villa': 1.3,
            'independent': 1.1
        }
        
        # Floor premium for apartments
        df['Floor_Multiplier'] = np.where(df['Property_Type'] == 'apartment',
                                        np.where(df['Floor_Number'] <= 3, 0.95,
                                                np.where(df['Floor_Number'] <= 8, 1.0, 1.05)),
                                        1.0)
        
        # Construction quality multipliers
        quality_multipliers = {
            'premium': 1.25,
            'good': 1.15,
            'standard': 1.0,
            'basic': 0.85
        }
        
        # Calculate price per sq.ft with all factors
        df['Price_Per_Sqft'] = (
            base_price_per_sqft *
            df['Location_Code'].map(location_multipliers) *
            df['Proximity_To_Main_Road'].map(proximity_multipliers) *
            df['Property_Type'].map(property_type_multipliers) *
            df['Floor_Multiplier'] *
            df['Construction_Quality'].map(quality_multipliers)
        )
        
        # Add feature adjustments to price per sq.ft (smaller adjustments)
        df['Price_Per_Sqft'] += (df['Bedrooms'] - 3) * 100  # ±100 per sq.ft per bedroom
        df['Price_Per_Sqft'] += (df['Bathrooms'] - 2) * 75   # ±75 per sq.ft per bathroom
        df['Price_Per_Sqft'] += (df['Garage_Size'] - 1) * 50   # ±50 per sq.ft per parking
        df['Price_Per_Sqft'] += (df['Condition_Rating'] - 3) * 150  # ±150 per sq.ft per condition
        df['Price_Per_Sqft'] += (df['Neighborhood_Score'] - 7) * 100  # ±100 per sq.ft per neighborhood point
        df['Price_Per_Sqft'] += (df['Walkability_Score'] - 8) * 75   # ±75 per sq.ft per walkability point
        
        # Ensure reasonable price per sq.ft range (₹3,000 - ₹15,000)
        df['Price_Per_Sqft'] = np.clip(df['Price_Per_Sqft'], 3000, 15000)
        
        # Calculate total price
        df['Sale_Price'] = df['Price_Per_Sqft'] * df['Living_Area']
        
        # Add market variation (±3% to reduce instability)
        market_variation = np.random.normal(0, 0.03, n_samples)
        df['Sale_Price'] *= (1 + market_variation)
        
        # Add historical trend (properties built earlier are cheaper)
        age_factor = (2023 - df['Year_Built']) * 0.01  # 1% depreciation per year (reduced)
        df['Sale_Price'] *= (1 - age_factor)
        
        # Ensure positive prices and reasonable range (₹10L - ₹10Cr)
        df['Sale_Price'] = np.clip(df['Sale_Price'].abs(), 1000000, 100000000)
        
        # Add climate multiplier (smaller impact)
        climate_multipliers = {
            'tropical': 1.02,
            'moderate': 1.0,
            'cold': 0.98,
            'arid': 0.95
        }
        df['Climate_Multiplier'] = df['Climate_Zone'].map(climate_multipliers)
        df['Sale_Price'] *= df['Climate_Multiplier']
        
        # Final price clipping to prevent extreme values
        df['Sale_Price'] = np.clip(df['Sale_Price'], 500000, 50000000)
        
        print(f"Sample dataset created with {n_samples} records")
        print(f"Columns: {list(df.columns)}")
        
        return df
    
    def preprocess_data(self, data):
        """Preprocess the dataset"""
        print("\n" + "="*40)
        print("DATA PREPROCESSING")
        print("="*40)
        
        processed_data = data.copy()
        
        # Handle missing values
        print("Handling missing values...")
        numeric_columns = processed_data.select_dtypes(include=[np.number]).columns
        categorical_columns = processed_data.select_dtypes(include=['object']).columns
        
        if len(numeric_columns) > 0:
            imputer = SimpleImputer(strategy='median')
            processed_data[numeric_columns] = imputer.fit_transform(processed_data[numeric_columns])
        
        if len(categorical_columns) > 0:
            imputer = SimpleImputer(strategy='most_frequent')
            processed_data[categorical_columns] = imputer.fit_transform(processed_data[categorical_columns])
        
        # Encode categorical variables
        print("Encoding categorical variables...")
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            processed_data[col] = self.label_encoders[col].fit_transform(processed_data[col])
        
        # Feature engineering
        print("Creating engineered features...")
        current_year = datetime.now().year
        if 'Year_Built' in processed_data.columns:
            processed_data['Property_Age'] = current_year - processed_data['Year_Built']
        
        if 'Living_Area' in processed_data.columns and 'Lot_Size' in processed_data.columns:
            processed_data['Living_to_Lot_Ratio'] = processed_data['Living_Area'] / processed_data['Lot_Size']
        
        print(f"Preprocessing completed. Final shape: {processed_data.shape}")
        return processed_data
    
    def train_model(self, data):
        """Train the stacking ensemble model"""
        print("\n" + "="*40)
        print("MODEL TRAINING")
        print("="*40)
        
        # Preprocess data
        processed_data = self.preprocess_data(data)
        
        # Split features and target
        X = processed_data.drop(self.target_column, axis=1)
        y = processed_data[self.target_column]
        
        self.feature_columns = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define base models
        print("Initializing base models...")
        base_models = [
            ('gbr', GradientBoostingRegressor(
                n_estimators=self.gb_trees,
                learning_rate=self.learning_rate,
                random_state=42
            )),
            ('rfr', RandomForestRegressor(
                n_estimators=self.rf_trees,
                random_state=42
            )),
            ('knn', KNeighborsRegressor(
                n_neighbors=self.knn_neighbors
            )),
            ('ridge', Ridge(alpha=1.0))
        ]
        
        # Create stacking ensemble
        print("Creating stacking ensemble...")
        self.model = StackingRegressor(
            estimators=base_models,
            final_estimator=RidgeCV(),
            cv=self.k_folds
        )
        
        # Train model
        print("Training model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        self.model_metrics = {
            'RMSE': rmse,
            'MAE': mae,
            'R2_Score': r2,
            'MAPE': mape
        }
        
        # Display results
        print("\nTraining completed!")
        print("\nModel Performance Metrics:")
        print("-" * 30)
        print(f"RMSE: ₹{rmse:,.2f}")
        print(f"MAE:  ₹{mae:,.2f}")
        print(f"R² Score: {r2:.4f}")
        print(f"MAPE: {mape:.2f}%")
        
        # Cross-validation scores
        print("\nCross-validation scores:")
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, 
                                   cv=self.k_folds, scoring='r2')
        print(f"CV R² scores: {[f'{score:.4f}' for score in cv_scores]}")
        print(f"Mean CV R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return self.model
    
    def predict_property(self, features):
        """Make prediction for a single property using ML model"""
        try:
            # Convert features to DataFrame
            input_df = pd.DataFrame([features])
            
            # Apply same preprocessing as training data
            processed_input = self.preprocess_single_input(input_df)
            
            # Scale features
            if self.scaler is None:
                raise ValueError("Model not trained yet. Call train_model() first.")
                
            input_scaled = self.scaler.transform(processed_input)
            
            # Make prediction
            predicted_price = self.model.predict(input_scaled)[0]
            
            # Ensure positive price
            predicted_price = max(0, predicted_price)
            
            return predicted_price
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            # Calculate a dynamic price based on input features instead of fixed default
            return self.calculate_fallback_price(features)
    
    def calculate_fallback_price(self, features):
        """Calculate a reasonable fallback price based on input features"""
        try:
            # Base price per sq.ft based on location
            location_multiplier = {
                'A': 15000,  # Prime location
                'B': 12000,  # Good location  
                'C': 8000,   # Average location
                'D': 5000    # Developing location
            }.get(features.get('Location_Code', 'C'), 8000)
            
            # Adjust for property type
            type_multiplier = {
                'apartment': 1.0,
                'villa': 1.5,
                'independent': 1.3
            }.get(features.get('Property_Type', 'apartment'), 1.0)
            
            # Get living area
            living_area = float(features.get('Living_Area', 1850))
            
            # Calculate base price
            base_price = living_area * location_multiplier * type_multiplier
            
            # Adjust for condition
            condition_rating = float(features.get('Condition_Rating', 3))
            condition_multiplier = 0.8 + (condition_rating / 5) * 0.4  # 0.8 to 1.2
            base_price *= condition_multiplier
            
            # Adjust for age
            year_built = int(features.get('Year_Built', 2020))
            current_year = datetime.now().year
            property_age = current_year - year_built
            age_multiplier = max(0.7, 1.0 - (property_age * 0.01))  # Decrease 1% per year, min 70%
            base_price *= age_multiplier
            
            # Add premium for amenities
            bedrooms = int(features.get('Bedrooms', 3))
            bathrooms = int(features.get('Bathrooms', 2))
            garage_size = int(features.get('Garage_Size', 1))
            
            bedroom_bonus = bedrooms * 100000  # 1 lakh per bedroom
            bathroom_bonus = bathrooms * 75000   # 75k per bathroom
            garage_bonus = garage_size * 50000   # 50k per garage space
            
            final_price = base_price + bedroom_bonus + bathroom_bonus + garage_bonus
            
            # Ensure reasonable range
            final_price = max(1000000, min(50000000, final_price))  # 10 lakhs to 5 crores
            
            return final_price
            
        except Exception as e:
            print(f"Fallback calculation error: {str(e)}")
            # Ultimate fallback based on living area
            living_area = float(features.get('Living_Area', 1850))
            return living_area * 8000  # 8000 per sq.ft average
    
    def preprocess_single_input(self, input_df):
        """Preprocess single input for prediction"""
        processed_input = input_df.copy()
        
        # Encode categorical variables
        categorical_columns = processed_input.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col in self.label_encoders:
                # Handle unseen categories
                unique_values = set(self.label_encoders[col].classes_)
                if processed_input[col].iloc[0] not in unique_values:
                    # Use most common category for unseen values
                    processed_input[col] = self.label_encoders[col].classes_[0]
                processed_input[col] = self.label_encoders[col].transform(processed_input[col])
            else:
                # Default to 0 for unknown categorical columns
                processed_input[col] = 0
        
        # Feature engineering
        current_year = datetime.now().year
        if 'Year_Built' in processed_input.columns:
            processed_input['Property_Age'] = current_year - processed_input['Year_Built']
        
        if 'Living_Area' in processed_input.columns and 'Lot_Size' in processed_input.columns:
            processed_input['Living_to_Lot_Ratio'] = processed_input['Living_Area'] / processed_input['Lot_Size']
        
        return processed_input
    
    def predict_property_price(self):
        """Interactive property price prediction"""
        print("\n" + "="*40)
        print("PREDICT PROPERTY PRICE")
        print("="*40)
        
        if self.model is None:
            print("Error: Model not trained yet. Please train the model first.")
            return
        
        print("Enter Property Details:")
        print("-" * 25)
        
        try:
            # Get user input
            property_data = {}
            
            # Required features with defaults
            bedrooms = int(input("Bedrooms: "))
            area = float(input("Living Area (sq.ft): "))
            lot = float(input("Lot Size (sq.ft): "))
            year = int(input("Year Built: "))
            condition = int(input("Condition Rating: "))
            location = input("Location Code: ").strip().upper()
            garage = int(input("Garage Size: "))
            bathrooms = int(input("Bathrooms: "))
            
            property_data = {
                'Bedrooms': bedrooms,
                'Living_Area': area,
                'Lot_Size': lot,
                'Year_Built': year,
                'Condition_Rating': condition,
                'Location_Code': location,
                'Garage_Size': garage,
                'Bathrooms': bathrooms
            }
            for feature in self.feature_columns:
                if feature in ['Property_Age', 'Living_to_Lot_Ratio']:
                    continue  # Skip engineered features
                
                default = feature_defaults.get(feature, '')
                prompt = f"{feature.replace('_', ' ')}"
                if default != '':
                    prompt += f" (default: {default})"
                prompt += ": "
                
                user_input = input(prompt).strip()
                
                if user_input == '':
                    value = default
                else:
                    if feature == 'Location_Code':
                        value = user_input.upper()
                    else:
                        value = float(user_input) if '.' in user_input else int(user_input)
                
                property_data[feature] = value
            
            # Create engineered features
            current_year = datetime.now().year
            if 'Year_Built' in property_data:
                property_data['Property_Age'] = current_year - property_data['Year_Built']
            
            if 'Living_Area' in property_data and 'Lot_Size' in property_data:
                property_data['Living_to_Lot_Ratio'] = property_data['Living_Area'] / property_data['Lot_Size']
            
            # Create DataFrame in correct order
            input_df = pd.DataFrame([property_data])
            
            # Ensure all required columns are present
            for col in self.feature_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = input_df[self.feature_columns]
            
            # Encode categorical variables
            for col, encoder in self.label_encoders.items():
                if col in input_df.columns:
                    try:
                        input_df[col] = encoder.transform(input_df[col])
                    except ValueError:
                        # Handle unseen categories
                        input_df[col] = 0
            
            # Scale features
            input_scaled = self.scaler.transform(input_df)
            
            # Make prediction
            predicted_price = self.model.predict(input_scaled)[0]
            
            # Display results
            print("\n" + "="*40)
            print("PREDICTION RESULTS")
            print("="*40)
            print(f"Estimated Property Value: ₹{predicted_price:,.2f}")
            
            # Show confidence interval based on MAE
            confidence_lower = predicted_price - self.model_metrics.get('MAE', 0)
            confidence_upper = predicted_price + self.model_metrics.get('MAE', 0)
            print(f"Confidence Range: ₹{confidence_lower:,.2f} - ₹{confidence_upper:,.2f}")
            
        except Exception as e:
            print(f"Error during prediction: {e}")
    
    def view_model_metrics(self):
        """Display model performance metrics"""
        print("\n" + "="*40)
        print("MODEL METRICS")
        print("="*40)
        
        if not self.model_metrics:
            print("No model metrics available. Please train the model first.")
            return
        
        print("Performance Metrics:")
        print("-" * 30)
        print(f"Root Mean Square Error (RMSE): ₹{self.model_metrics['RMSE']:,.2f}")
        print(f"Mean Absolute Error (MAE): ₹{self.model_metrics['MAE']:,.2f}")
        print(f"R² Score: {self.model_metrics['R2_Score']:.4f}")
        print(f"Mean Absolute Percentage Error (MAPE): {self.model_metrics['MAPE']:.2f}%")
        
        print(f"\nModel Configuration:")
        print("-" * 30)
        print(f"K-Fold Cross Validation: {self.k_folds} folds")
        print(f"Random Forest Trees: {self.rf_trees}")
        print(f"Gradient Boosting Trees: {self.gb_trees}")
        print(f"Learning Rate: {self.learning_rate}")
        print(f"K-Nearest Neighbors: {self.knn_neighbors} neighbors")
        
        if self.feature_columns:
            print(f"\nFeatures Used ({len(self.feature_columns)}):")
            print("-" * 30)
            for i, feature in enumerate(self.feature_columns, 1):
                print(f"{i:2d}. {feature}")
    
    def save_model(self):
        """Save trained model to file"""
        if self.model is None:
            print("No model to save. Please train the model first.")
            return
        
        filename = input("Enter filename to save model (default: spvp_model.pkl): ").strip()
        if not filename:
            filename = "spvp_model.pkl"
        
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns,
                'target_column': self.target_column,
                'model_metrics': self.model_metrics,
                'hyperparameters': {
                    'k_folds': self.k_folds,
                    'rf_trees': self.rf_trees,
                    'gb_trees': self.gb_trees,
                    'learning_rate': self.learning_rate,
                    'knn_neighbors': self.knn_neighbors
                }
            }
            
            with open(filename, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"Model saved successfully to '{filename}'")
            
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model from file"""
        filename = input("Enter filename to load model: ").strip()
        
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return
        
        try:
            with open(filename, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.label_encoders = model_data['label_encoders']
            self.feature_columns = model_data['feature_columns']
            self.target_column = model_data['target_column']
            self.model_metrics = model_data['model_metrics']
            
            # Load hyperparameters
            if 'hyperparameters' in model_data:
                params = model_data['hyperparameters']
                self.k_folds = params.get('k_folds', 5)
                self.rf_trees = params.get('rf_trees', 100)
                self.gb_trees = params.get('gb_trees', 100)
                self.learning_rate = params.get('learning_rate', 0.1)
                self.knn_neighbors = params.get('knn_neighbors', 5)
            
            print(f"Model loaded successfully from '{filename}'")
            self.view_model_metrics()
            
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def save_load_menu(self):
        """Save/Load model submenu"""
        while True:
            print("\nSAVE/LOAD MODEL")
            print("-" * 20)
            print("1. Save Model")
            print("2. Load Model")
            print("3. Back to Main Menu")
            print("-" * 20)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.save_model()
            elif choice == '2':
                self.load_model()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def run(self):
        """Main application loop"""
        self.display_header()
        
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                data = self.load_dataset()
                if data is not None:
                    self.current_data = data
                    print("\nDataset ready for training!")
                    
            elif choice == '2':
                if not hasattr(self, 'current_data'):
                    print("No dataset loaded. Please upload a dataset first.")
                else:
                    self.train_model(self.current_data)
                    
            elif choice == '3':
                self.predict_property_price()
                
            elif choice == '4':
                self.view_model_metrics()
                
            elif choice == '5':
                self.save_load_menu()
                
            elif choice == '6':
                print("\nThank you for using Smart Property Value Predictor!")
                print("Goodbye!")
                break
                
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    try:
        app = SmartPropertyValuePredictor()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
