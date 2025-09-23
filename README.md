# Smart Menu

## Run CLI demo

```
pip install -r requirements.txt
python -m src.main --user 1 --time dinner --budget mid --top 10
```

## Run API server

```
uvicorn src.api:app --reload
```

Test:
```
curl "http://127.0.0.1:8000/recommendations?user_id=1&time=lunch&budget=low&top=10"
curl "http://127.0.0.1:8000/notifications?user_id=1"
```

## Django integration
Use helpers in `src/django_integration.py` to convert QuerySets to DataFrames and pass them to the hybrid recommender from your views.

