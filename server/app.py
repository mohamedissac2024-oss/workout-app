from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

# ---------- App setup ----------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

workout_schema = WorkoutSchema()
exercise_schema = ExerciseSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def save(obj):
    """Add an object to the database; return an error response or None."""
    try:
        db.session.add(obj)
        db.session.commit()
    except ValueError as err:          # model validation failed
        db.session.rollback()
        return jsonify({'error': str(err)}), 400
    except IntegrityError:             # table constraint failed
        db.session.rollback()
        return jsonify({'error': 'Database constraint failed (duplicate or invalid data).'}), 400
    return None


# ---------- Home ----------
@app.route('/')
def index():
    return jsonify({
        'message': 'Workout Tracker API',
        'endpoints': ['/workouts', '/exercises']
    }), 200


# ---------- Workouts ----------
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workout_schema.dump(workouts, many=True)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        workout = Workout(**data)
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

    error = save(workout)
    if error:
        return error
    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    db.session.delete(workout)
    db.session.commit()
    return '', 204


# ---------- Exercises ----------
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercise_schema.dump(exercises, many=True)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        exercise = Exercise(**data)
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

    error = save(exercise)
    if error:
        return error
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    db.session.delete(exercise)
    db.session.commit()
    return '', 204


# ---------- Add an exercise to a workout ----------
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    try:
        data = workout_exercise_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

    error = save(link)
    if error:
        return error
    return jsonify(workout_exercise_schema.dump(link)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)