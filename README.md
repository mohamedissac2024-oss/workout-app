# Workout Tracker API

## Description
A backend API for a workout tracking application used by personal trainers.
It tracks workouts and reusable exercises, and lets you add an exercise to a
workout with sets and reps, or a duration. Built with Flask, SQLAlchemy and
Marshmallow.

## Features
- Create, view and delete workouts
- Create, view and delete exercises
- Add an exercise to a workout (sets + reps, or a duration)
- Validation at three levels: table constraints, model validations and schema validations
- Seed file with example data

## Project Structure
```
workout-app/
├── Pipfile
├── Pipfile.lock
├── README.md
└── server/
    ├── app.py        # Flask app and endpoints
    ├── models.py     # SQLAlchemy models and relationships
    ├── schemas.py    # Marshmallow schemas
    ├── seed.py       # Example data
    └── migrations/   # Database migrations
```

## Installation
1. Clone the repository and move into it:
```
   git clone git@github.com:mohamedissac2024-oss/workout-app.git
   cd workout-app
```
2. Install dependencies and enter the virtual environment:
```
   pipenv install
   pipenv shell
```
3. Set up the database and seed it:
```
   cd server
   export FLASK_APP=app.py
   flask db upgrade
   python seed.py
```

## Run
From the `server/` folder:
```
flask run
```
The API runs at `http://127.0.0.1:5000`.

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Welcome message and list of endpoints |
| GET | `/workouts` | List all workouts with their exercises |
| GET | `/workouts/<id>` | Get one workout (404 if not found) |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get one exercise (404 if not found) |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

### Example requests
Create an exercise:
```
curl -X POST http://127.0.0.1:5000/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Lunge", "category": "Strength"}'
```

Create a workout:
```
curl -X POST http://127.0.0.1:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-10-17", "duration_minutes": 40}'
```

Add an exercise to a workout:
```
curl -X POST http://127.0.0.1:5000/workouts/1/exercises/3/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"sets": 3, "reps": 10}'
```

## Validations

**Table constraints**
- Exercise name is# workout-app
