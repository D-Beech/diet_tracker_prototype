from sqlalchemy.orm import Session
from db.models import LogEntry as LogEntryModel, Exercise as ExerciseModel, Food as FoodModel
from services.models import LogEntry  # Pydantic

def save_log_entry(db: Session, log: LogEntry) -> LogEntryModel:
    db_log = LogEntryModel(
        body_weight_kg=log.body_weight_kg,
        timestamp=log.timestamp
    )

    for e in log.exercise:
        db_log.exercises.append(
            ExerciseModel(
                name=e.name,
                sets=e.sets,
                reps=e.reps,
                weight_kg=e.weight_kg,
                distance_km=e.distance_km,
                time_min=e.time_min
            )
        )

    for f in log.food:
        db_log.foods.append(
            FoodModel(
                name=f.name,
                quantity_g=f.quantity_g,
                quantity_items=f.quantity_items
            )
        )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log
