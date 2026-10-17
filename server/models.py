from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()

CATEGORIES = ['Strength', 'Cardio', 'Flexibility', 'Balance']


class Exercise(db.Model):
    __tablename__ = 'exercises'

    # table constraint: name must be at least 2 characters
    __table_args__ = (
        CheckConstraint('length(name) >= 2', name='name_length'),
    )

    id = db.Column(db.Integer, primary_key=True)
    # table constraints: required and unique
    name = db.Column(db.String(50), nullable=False, unique=True)
    category = db.Column(db.String(20), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # deleting an exercise also deletes its links to workouts
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Exercise name must be at least 2 characters.')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if category not in CATEGORIES:
            raise ValueError(f'Category must be one of: {", ".join(CATEGORIES)}.')
        return category

    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    # table constraint: a workout must last longer than 0 minutes
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='positive_duration'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(200))

    # deleting a workout also deletes its links to exercises
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )

    @validates('duration_minutes')
    def validate_duration(self, key, minutes):
        if minutes is None or minutes <= 0:
            raise ValueError('Duration must be greater than 0 minutes.')
        return minutes

    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 200:
            raise ValueError('Notes must be 200 characters or less.')
        return notes

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}>'


class WorkoutExercise(db.Model):
    """Join table: one exercise inside one workout, with sets/reps/duration."""
    __tablename__ = 'workout_exercises'

    __table_args__ = (
        # the same exercise can't be added to the same workout twice
        UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
        CheckConstraint('reps IS NULL OR reps > 0', name='positive_reps'),
        CheckConstraint('sets IS NULL OR sets > 0', name='positive_sets'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f'{key} must be greater than 0.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}, workout={self.workout_id}, exercise={self.exercise_id}>'