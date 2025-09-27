from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
from typing import Optional
from .contextual import Context
from .hybrid import recommend as base_recommend
<<<<<<< HEAD
from .hybrid_recommender import get_hybrid_recommender
=======
from .smart_recommender import get_smart_recommender
from .smart_query_processor import get_query_processor
>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
from .notifications import generate_notifications
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Menu API - Hackathon Edition", version="2.0.0")


@app.get("/recommendations")
def get_recommendations(
    user_id: int, 
    time: str | None = Query(None), 
    budget: str | None = Query(None), 
    top: int = 10,
<<<<<<< HEAD
    include_explanation: bool = Query(False, description="Include explanation"),
    use_hybrid: bool = Query(True, description="Use hybrid recommendation system")
=======
    query: str | None = Query(None, description="Natural language query for recommendations"),
    include_explanation: bool = Query(False, description="Include AI-generated explanation"),
    use_smart: bool = Query(True, description="Use smart recommendation system")
>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
):
    """Get personalized menu recommendations"""
    try:
        ctx = Context(user_id=user_id, now=datetime.now(), time_of_day=time, budget_level=budget)
        
<<<<<<< HEAD
        if use_hybrid:
            # Use hybrid system
            recommender = get_hybrid_recommender()
=======
        if use_smart:
            # Use smart system with impressive features
            recommender = get_smart_recommender()
>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
            result = recommender.get_recommendations(
                user_id=user_id,
                top_k=top,
                context=ctx,
<<<<<<< HEAD
=======
                user_query=query,
>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
                include_explanation=include_explanation
            )
            return result
        else:
            # Use original system
            df = base_recommend(user_id, top_k=top, ctx=ctx)
            return {
                "recommendations": df.to_dict(orient="records"),
                "metadata": {
                    "user_id": user_id,
                    "time_of_day": ctx.time_of_day,
                    "budget_level": ctx.budget_level,
                    "total_recommendations": len(df),
                    "from_cache": False,
                    "processing_time_seconds": 0.0,
                    "timestamp": datetime.now().isoformat()
                }
            }
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications")
def get_notifications(user_id: int):
    """Get personalized notifications for user"""
    try:
        return {"notifications": generate_notifications(user_id)}
    except Exception as e:
        logger.error(f"Error generating notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
def record_feedback(
    user_id: int,
    item_id: int,
    feedback_type: str,
    value: float,
    metadata: dict | None = None
):
    """Record user feedback for learning"""
    try:
<<<<<<< HEAD
        recommender = get_hybrid_recommender()
=======
        recommender = get_smart_recommender()
>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
        recommender.record_feedback(user_id, item_id, value, feedback_type)
        return {"status": "success", "message": "Feedback recorded"}
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_system_metrics():
    """Get system performance metrics"""
    try:
<<<<<<< HEAD
        recommender = get_hybrid_recommender()
=======
        recommender = get_smart_recommender()
>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
        return recommender.get_system_stats()
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


<<<<<<< HEAD
=======
@app.get("/query-analysis")
def analyze_query(query: str):
    """Analyze natural language query"""
    try:
        processor = get_query_processor()
        result = processor.process_query(query, user_id=1)  # Demo user
        return result
    except Exception as e:
        logger.error(f"Error analyzing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


>>>>>>> 2929a20c83374885c753a507262aca7b42e52660
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }




