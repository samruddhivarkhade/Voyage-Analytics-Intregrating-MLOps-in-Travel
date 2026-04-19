from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import json
import time
from datetime import datetime
from app.schemas.input_schema import (
    FlightPriceRequest,
    FlightPriceResponse,
    GenderRequest,
    GenderResponse,
    HotelRecommendationRequest,
    HotelRecommendationResponse,
    HotelRecommendation,
    UserStats
)
from app.core.database import get_db
from app.core.models import Prediction
from app.services.preprocess import build_feature_vector, build_gender_feature_vector
from app.services.predictor import run_prediction, predict_gender
from app.services.hotel_recommendation import HotelRecommendationInference
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Import get_current_user from auth for protected endpoints
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current authenticated user"""
    from app.api.auth import get_current_user as auth_get_current_user
    return auth_get_current_user(request, db)


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/predict", response_model=FlightPriceResponse)
def predict_flight_price(payload: FlightPriceRequest, request: Request, db: Session = Depends(get_db), user = Depends(get_current_user)):
    logger.info(
        "Incoming prediction request | client=%s | payload=%s",
        request.client.host,
        payload.model_dump(),
    )

    start_time = time.time()
    model = request.app.state.model
    encoders = request.app.state.encoders
    target_encodings = request.app.state.target_encodings
    selected_features = request.app.state.selected_features

    feature_vector = build_feature_vector(payload, encoders, target_encodings, selected_features)
    predicted_price = run_prediction(model, feature_vector)

    # Save prediction to database
    try:
        prediction = Prediction(
            user_id=user.id,
            model_type='flight',
            input_data=json.dumps(payload.model_dump()),
            output_data=json.dumps({'predicted_price': float(predicted_price)})
        )
        db.add(prediction)
        db.commit()
        logger.info(f"Prediction saved to database for user {user.id}")
    except Exception as e:
        logger.error(f"Failed to save prediction: {e}")
        db.rollback()

    logger.info("Prediction response | predicted_price=%.4f", predicted_price)
    return FlightPriceResponse(predicted_price=predicted_price)






@router.post("/predict-gender", response_model=GenderResponse)
def predict_gender_api(payload: GenderRequest, request: Request, db: Session = Depends(get_db), user = Depends(get_current_user)):
    logger.info(
        "Incoming gender prediction | client=%s | payload=%s",
        request.client.host,
        payload.model_dump(),
    )

    feature_vector = payload.model_dump()
    predicted_gender = predict_gender(feature_vector)

    # Save prediction to database
    try:
        prediction = Prediction(
            user_id=user.id,
            model_type='gender',
            input_data=json.dumps(payload.model_dump()),
            output_data=json.dumps({'predicted_gender': predicted_gender})
        )
        db.add(prediction)
        db.commit()
        logger.info(f"Gender prediction saved to database for user {user.id}")
    except Exception as e:
        logger.error(f"Failed to save prediction: {e}")
        db.rollback()

    logger.info("Gender prediction response | gender=%s", predicted_gender)

    return GenderResponse(predicted_gender=predicted_gender)


@router.get("/stats", response_model=UserStats)
def get_user_stats(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Get user prediction statistics"""
    logger.info(f"Fetching stats for user {user.id}")
    
    # Get all predictions for the user
    predictions = db.query(Prediction).filter(Prediction.user_id == user.id).all()
    
    total_predictions = len(predictions)
    flight_predictions = len([p for p in predictions if p.model_type == 'flight'])
    gender_predictions = len([p for p in predictions if p.model_type == 'gender'])
    
    # Get last prediction time
    last_prediction = None
    if predictions:
        latest = max(predictions, key=lambda p: p.created_at)
        last_prediction = latest.created_at.isoformat() if latest.created_at else None
    
    logger.info(
        f"User stats | total={total_predictions} | flight={flight_predictions} | gender={gender_predictions}"
    )
    
    return UserStats(
        total_predictions=total_predictions,
        flight_predictions=flight_predictions,
        gender_predictions=gender_predictions,
        avg_prediction_time_ms=0.0,
        last_prediction=last_prediction
    )


@router.post("/recommend-hotels", response_model=HotelRecommendationResponse)
def recommend_hotels(payload: HotelRecommendationRequest, request: Request):
    """
    Get personalized hotel recommendations based on user profile
    
    Parameters:
    -----------
    days : int - Number of days staying (1-30)
    month : int - Travel month (1-12)
    age : int - User age (18-100)
    gender : str - 'male', 'female', or 'unknown'
    budget : str - 'budget', 'mid', or 'luxury'
    company : str - One of: 4You, Acme Factory, Monsters CYA, Umbrella LTDA, Wonka Company
    top_n : int - Number of recommendations to return (default: 5)
    
    Returns:
    --------
    HotelRecommendationResponse with list of recommended hotels and match scores
    """
    logger.info(
        "Incoming hotel recommendation request | client=%s | payload=%s",
        request.client.host,
        payload.model_dump(),
    )
    
    try:
        # Load recommendation model
        if not hasattr(request.app.state, 'hotel_recommender'):
            logger.info("Loading hotel recommendation model")
            request.app.state.hotel_recommender = HotelRecommendationInference()
        
        recommender = request.app.state.hotel_recommender
        
        # Get recommendations
        recommendations = recommender.recommend(
            days=payload.days,
            month=payload.month,
            age=payload.age,
            gender=payload.gender,
            budget=payload.budget,
            company=payload.company,
            top_n=payload.top_n
        )
        
        # Convert to response format
        hotel_recommendations = [
            HotelRecommendation(
                rank=rec['rank'],
                hotel=rec['hotel'],
                match_score=rec['match_score']
            )
            for rec in recommendations
        ]
        
        logger.info(
            "Hotel recommendation response | count=%d | user_profile=%s-%s-%s",
            len(hotel_recommendations),
            payload.gender,
            payload.budget,
            payload.company
        )
        
        return HotelRecommendationResponse(
            recommendations=hotel_recommendations,
            total_recommendations=len(hotel_recommendations)
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except FileNotFoundError as e:
        logger.error(f"Model not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Hotel recommendation model not trained yet"
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate hotel recommendations"
        )
