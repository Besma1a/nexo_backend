from fastapi import FastAPI, Query
from datetime import datetime
from .contextual import Context
from .hybrid import recommend
from .notifications import generate_notifications


app = FastAPI(title="Smart Menu API")


@app.get("/recommendations")
def get_recommendations(user_id: int, time: str | None = Query(None), budget: str | None = Query(None), top: int = 10):
    ctx = Context(user_id=user_id, now=datetime.now(), time_of_day=time, budget_level=budget)
    df = recommend(user_id, top_k=top, ctx=ctx)
    return {"recommendations": df.to_dict(orient="records")}


@app.get("/notifications")
def get_notifications(user_id: int):
    return {"notifications": generate_notifications(user_id)}



