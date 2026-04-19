"""
Hotel Recommendation Service
Trains and manages the hotel recommendation model using RandomForest
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Hotel recommendation model constants
MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "hotel_recommendation"
MODEL_FILE = MODEL_PATH / "hotel_recommender.pkl"
DATA_PATH = Path(__file__).parent.parent.parent.parent / "data"

ALL_COMPANIES = ['4You', 'Acme Factory', 'Monsters CYA', 'Umbrella LTDA', 'Wonka Company']


class HotelRecommendationPipeline:
    """Training pipeline for hotel recommendation model"""
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.hotel_encoder = None
        self.company_cols = []
        self.numeric_features = ['days', 'month', 'age']
        self.categorical_features = []
        self.artifacts = {}

    def load_and_prepare_data(self):
        """Load and prepare training data"""
        logger.info("Loading data from CSV files")
        
        try:
            users = pd.read_csv(DATA_PATH / "users.csv")
            hotels = pd.read_csv(DATA_PATH / "hotels.csv")
            
            logger.info(f"Users dataset shape: {users.shape}")
            logger.info(f"Hotels dataset shape: {hotels.shape}")
        except FileNotFoundError as e:
            logger.error(f"Data files not found: {e}")
            raise
        
        # Fix gender values
        users['gender'] = users['gender'].replace('none', 'unknown')
        logger.info(f"Gender distribution: {users['gender'].value_counts().to_dict()}")
        
        # Merge datasets
        hotels.rename(columns={"name": "hotel_name"}, inplace=True)
        df = hotels.merge(
            users[["code", "age", "gender", 'company']],
            left_on='userCode',
            right_on='code',
            how='left'
        )
        df.drop(columns=['userCode', 'code', 'travelCode', 'total'], inplace=True)
        
        logger.info(f"Merged dataset shape: {df.shape}")
        return df
    
    def feature_engineering(self, df):
        """Perform feature engineering"""
        logger.info("Starting feature engineering")
        
        # Create month column
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['month'] = df['date'].dt.month
        df.drop(columns=['date'], inplace=True)
        
        # Create price tier
        def price_tier(price):
            if price <= 180:
                return "budget"
            elif price <= 250:
                return "mid"
            else:
                return "luxury"
        
        df['price_tier'] = df['price'].apply(price_tier)
        
        # Remove leakage columns
        df.drop(columns=['place', 'price'], inplace=True)
        
        # Remove nulls
        initial_shape = df.shape
        df.dropna(inplace=True)
        logger.info(f"Rows before/after null removal: {initial_shape[0]} -> {df.shape[0]}")
        
        return df
    
    def encode_features(self, df):
        """Encode categorical features"""
        logger.info("Encoding categorical features")
        
        # One-hot encode company
        company_dummies = pd.get_dummies(df['company'], prefix='co').astype(int)
        df = pd.concat([df.drop('company', axis=1), company_dummies], axis=1)
        self.company_cols = list(company_dummies.columns)
        logger.info(f"Company columns: {self.company_cols}")
        
        # Label encode gender and price_tier
        for col in ['gender', 'price_tier']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.encoders[col] = le
            logger.info(f"{col} classes: {list(le.classes_)}")
        
        # Encode target
        self.hotel_encoder = LabelEncoder()
        df['hotel_name'] = self.hotel_encoder.fit_transform(df['hotel_name'])
        logger.info(f"Hotels: {list(self.hotel_encoder.classes_)}")
        
        return df
    
    def train(self, df):
        """Train the recommendation model"""
        logger.info("Training RandomForest model for hotel recommendation")
        
        self.categorical_features = ['gender', 'price_tier'] + self.company_cols
        feature_cols = self.numeric_features + self.categorical_features
        
        X = df[feature_cols]
        y = df['hotel_name']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")
        
        self.model = RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        logger.info("Model training complete")
        
        # Evaluate
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logger.info(f"Model accuracy: {accuracy:.2%}")
        logger.info("Classification Report:")
        logger.info(classification_report(y_test, predictions, 
                                         target_names=self.hotel_encoder.classes_))
        
        return X_test, y_test
    
    def evaluate_top_k_accuracy(self, X_test, y_test):
        """Evaluate top-k recommendation accuracy"""
        probabilities = self.model.predict_proba(X_test)
        y_true = y_test.values
        
        def topk_accuracy(proba, y_true, k):
            top_k = np.argsort(proba, axis=1)[:, -k:]
            hits = sum(y_true[i] in top_k[i] for i in range(len(y_true)))
            return hits / len(y_true)
        
        metrics = {
            'random_baseline': 1.0 / len(self.hotel_encoder.classes_),
            'top_1_accuracy': topk_accuracy(probabilities, y_true, 1),
            'top_3_accuracy': topk_accuracy(probabilities, y_true, 3),
            'top_5_accuracy': topk_accuracy(probabilities, y_true, 5),
        }
        
        logger.info("Recommendation System Metrics:")
        logger.info(f"  Random baseline: {metrics['random_baseline']:.2%}")
        logger.info(f"  Top-1 accuracy: {metrics['top_1_accuracy']:.2%}")
        logger.info(f"  Top-3 accuracy: {metrics['top_3_accuracy']:.2%}")
        logger.info(f"  Top-5 accuracy: {metrics['top_5_accuracy']:.2%}")
        
        return metrics
    
    def save_artifacts(self):
        """Save model and encoders"""
        logger.info("Saving model artifacts")
        
        MODEL_PATH.mkdir(parents=True, exist_ok=True)
        
        self.artifacts = {
            'model': self.model,
            'hotel_encoder': self.hotel_encoder,
            'encoders': self.encoders,
            'company_cols': self.company_cols,
            'numeric_features': self.numeric_features,
            'categorical_features': self.categorical_features
        }
        
        with open(MODEL_FILE, 'wb') as f:
            pickle.dump(self.artifacts, f)
        
        logger.info(f"Model saved to {MODEL_FILE}")
    
    def run_training_pipeline(self):
        """Execute the complete training pipeline"""
        logger.info("Starting hotel recommendation training pipeline")
        
        # Load and prepare data
        df = self.load_and_prepare_data()
        
        # Feature engineering
        df = self.feature_engineering(df)
        
        # Encode features
        df = self.encode_features(df)
        
        # Train model
        X_test, y_test = self.train(df)
        
        # Evaluate
        metrics = self.evaluate_top_k_accuracy(X_test, y_test)
        
        # Save artifacts
        self.save_artifacts()
        
        logger.info("Hotel recommendation training pipeline complete")
        return metrics


class HotelRecommendationInference:
    """Inference service for hotel recommendations"""
    
    def __init__(self):
        self.artifacts = None
        self.load_artifacts()
    
    def load_artifacts(self):
        """Load pre-trained model and encoders"""
        if not MODEL_FILE.exists():
            logger.warning(f"Model file not found: {MODEL_FILE}")
            raise FileNotFoundError(f"Hotel recommendation model not found at {MODEL_FILE}")
        
        with open(MODEL_FILE, 'rb') as f:
            self.artifacts = pickle.load(f)
        
        logger.info("Hotel recommendation artifacts loaded")
    
    def recommend(self, days: int, month: int, age: int, gender: str, 
                 budget: str, company: str, top_n: int = 5) -> list:
        """
        Recommend top hotels for a user
        
        Parameters:
        -----------
        days : int
            Number of days staying
        month : int
            Travel month (1-12)
        age : int
            User age
        gender : str
            'male', 'female', or 'unknown'
        budget : str
            'budget', 'mid', or 'luxury'
        company : str
            Company name
        top_n : int
            Number of recommendations to return
        
        Returns:
        --------
        list : List of recommended hotels with scores
        """
        mdl = self.artifacts['model']
        h_enc = self.artifacts['hotel_encoder']
        encs = self.artifacts['encoders']
        co_cols = self.artifacts['company_cols']
        num_feats = self.artifacts['numeric_features']
        cat_feats = self.artifacts['categorical_features']
        
        # Validate inputs
        if gender not in list(encs['gender'].classes_):
            logger.warning(f"Invalid gender: {gender}")
            raise ValueError(f"Invalid gender. Options: {list(encs['gender'].classes_)}")
        
        if budget not in list(encs['price_tier'].classes_):
            logger.warning(f"Invalid budget: {budget}")
            raise ValueError(f"Invalid budget. Options: {list(encs['price_tier'].classes_)}")
        
        if company not in ALL_COMPANIES:
            logger.warning(f"Invalid company: {company}")
            raise ValueError(f"Unknown company. Options: {ALL_COMPANIES}")
        
        # Encode inputs
        enc_gender = encs['gender'].transform([gender])[0]
        enc_budget = encs['price_tier'].transform([budget])[0]
        
        # One-hot encode company
        company_values = {col: int(col == f'co_{company}') for col in co_cols}
        
        # Build input DataFrame
        row = {
            'days': days,
            'month': month,
            'age': age,
            'gender': enc_gender,
            'price_tier': enc_budget
        }
        row.update(company_values)
        
        input_df = pd.DataFrame([row], columns=num_feats + cat_feats)
        
        # Predict probabilities
        proba = mdl.predict_proba(input_df)[0]
        
        # Rank top-N
        top_indices = proba.argsort()[-top_n:][::-1]
        recommendations = [
            {
                'rank': i + 1,
                'hotel': h_enc.inverse_transform([idx])[0],
                'match_score': round(float(proba[idx]) * 100, 2)
            }
            for i, idx in enumerate(top_indices)
        ]
        
        logger.info(f"Generated {len(recommendations)} recommendations for user: "
                   f"days={days}, month={month}, age={age}, gender={gender}, "
                   f"budget={budget}, company={company}")
        
        return recommendations


def load_recommendation_model():
    """Load hotel recommendation model for inference"""
    try:
        return HotelRecommendationInference()
    except Exception as e:
        logger.error(f"Failed to load recommendation model: {e}")
        return None
