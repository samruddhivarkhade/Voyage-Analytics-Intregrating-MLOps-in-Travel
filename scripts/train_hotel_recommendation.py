#!/usr/bin/env python
"""
Training script for Hotel Recommendation Model
Trains a RandomForest model to recommend hotels based on user profiles
"""

import sys
from pathlib import Path

# Add ml-service to path
ml_service_path = Path(__file__).parent.parent / "ml-service"
sys.path.insert(0, str(ml_service_path))

from app.services.hotel_recommendation import HotelRecommendationPipeline
from app.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Run the hotel recommendation training pipeline"""
    logger.info("=" * 70)
    logger.info("HOTEL RECOMMENDATION MODEL TRAINING")
    logger.info("=" * 70)
    
    try:
        # Initialize pipeline
        pipeline = HotelRecommendationPipeline()
        
        # Run training
        metrics = pipeline.run_training_pipeline()
        
        # Display results
        logger.info("=" * 70)
        logger.info("TRAINING COMPLETE - METRICS SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Random Baseline:  {metrics['random_baseline']:.2%}")
        logger.info(f"Top-1 Accuracy:   {metrics['top_1_accuracy']:.2%}")
        logger.info(f"Top-3 Accuracy:   {metrics['top_3_accuracy']:.2%}")
        logger.info(f"Top-5 Accuracy:   {metrics['top_5_accuracy']:.2%}")
        logger.info("=" * 70)
        
        return 0
    
    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())
