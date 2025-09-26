Notebooks Demo
==============

Prereqs
- Python env with requirements from `Hack/smart_menu/requirements.txt`
- Jupyter (e.g., `pip install jupyter`)

Run
1. cd to `Hack/smart_menu`
2. Start Django API in another terminal from project root:
   - `cd Hack`
   - `python manage.py runserver 0.0.0.0:8000`
3. Launch notebooks:
   - `jupyter notebook notebooks/`

Notebooks
- 00_Setup_and_Data_Check.ipynb: Load CSV demo data and run a quick recommendation using file-based loaders.
- 01_Data_Visualization.ipynb: Visualize categories, price distribution, and orders over time.
- 02_Recommendations_Demo.ipynb: Call live Django endpoint `/api/smart/recommendations/` and compare contexts.

Tips
- Ensure you have at least one user, items, and some orders in the DB for meaningful results.
- Use Django endpoints to add data:
  - POST `/api/user/add/`
  - POST `/api/orders/`


