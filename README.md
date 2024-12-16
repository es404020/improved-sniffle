# Expense Tracker API

## Project Setup

1. Clone the repository
```bash
git clone <your-repo-url>
cd expense_tracker
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server
```bash
python manage.py runserver
```

## API Endpoints

### Users
- `GET /users/`: List all users
- `POST /users/`: Create a new user
- `GET /users/<id>/`: Retrieve a specific user
- `PUT /users/<id>/`: Update a user
- `DELETE /users/<id>/`: Delete a user

### Expenses
- `GET /expenses/`: List all expenses
- `POST /expenses/`: Create a new expense
- `GET /expenses/<id>/`: Retrieve a specific expense
- `PUT /expenses/<id>/`: Update an expense
- `DELETE /expenses/<id>/`: Delete an expense

### Custom Endpoints
- `GET /users/<user_id>/expenses/date-range/`: 
  - List expenses within a specific date range
  - Query params: `start_date`, `end_date`

- `GET /users/<user_id>/expenses/category-summary/<year>/<month>/`: 
  - Get total expenses per category for a specific month

## API Documentation
Visit `/swagger/` or `/redoc/` for interactive API documentation.

## URL Reference
Run tests using:
```bash
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```