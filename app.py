from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI(title="Student Result Prediction API")

REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

class Student(BaseModel):
    study_hours: float = Field(ge=0, le=24)
    attendance: float = Field(ge=0, le=100)
    previous_score: float = Field(ge=0, le=100)
    assignments_completed: float = Field(ge=0, le=10)


@app.get("/")
def home():
    return {"message": "Student Result Prediction API is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model": "student-result-prediction"
    }


@app.post("/predict")
def predict(student: Student):
    REQUEST_COUNT.inc()

    score = (
        (student.study_hours / 24) * 30
        + (student.attendance / 100) * 30
        + (student.previous_score / 100) * 30
        + (student.assignments_completed / 10) * 10
    )

    score = round(score, 2)

    return {
        "predicted_score": score,
        "result": "Pass" if score >= 40 else "Fail"
    }


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
