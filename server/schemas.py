from marshmallow import Schema, fields, validate, validates_schema, ValidationError

CATEGORIES = ['Strength', 'Cardio', 'Flexibility', 'Balance']


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1), allow_none=True)

    # show a short version of the exercise (avoids looping back to the workout)
    exercise = fields.Nested(ExerciseSchema(only=('id', 'name', 'category')), dump_only=True)

    @validates_schema
    def check_effort(self, data, **kwargs):
        # a workout exercise needs either sets AND reps, or a duration
        has_sets_reps = data.get('sets') and data.get('reps')
        has_duration = data.get('duration_seconds')
        if not has_sets_reps and not has_duration:
            raise ValidationError('Provide both sets and reps, or a duration_seconds.')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(validate=validate.Length(max=200), allow_none=True)

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)