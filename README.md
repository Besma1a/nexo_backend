# Smart Menu Project

A Django-based smart menu system that provides personalized food recommendations.

## Setup

1. Clone the repository
```bash
git clone <repository-url>
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

## Features
- User questionnaire system
- Food recommendations
- Admin interface

## Technologies
- Python 3.x
- Django
- SQLite3

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


