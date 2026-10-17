from datetime import date

from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    # clear old data so the seed can be run again
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    squat = Exercise(name='Squat', category='Strength', equipment_needed=True)
    pushup = Exercise(name='Push-up', category='Strength', equipment_needed=False)
    running = Exercise(name='Running', category='Cardio', equipment_needed=False)
    yoga = Exercise(name='Yoga Flow', category='Flexibility', equipment_needed=False)

    leg_day = Workout(date=date(2026, 10, 12), duration_minutes=45, notes='Leg day')
    cardio_day = Workout(date=date(2026, 10, 14), duration_minutes=30, notes='Easy cardio')

    db.session.add_all([squat, pushup, running, yoga, leg_day, cardio_day])
    db.session.commit()

    links = [
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, sets=4, reps=10),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=pushup.id, sets=3, reps=15),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=running.id, duration_seconds=1200),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=yoga.id, duration_seconds=600),
    ]
    db.session.add_all(links)
    db.session.commit()

    print('Database seeded!')