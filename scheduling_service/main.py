from datetime import datetime

from fastapi import FastAPI
from scheduling_service.validation import validate_schedule
from pydantic import BaseModel, field_validator
from fastapi import HTTPException

app = FastAPI()

@app.get("/health")
async def root():
    return {"status": "ok"}

class ScheduleRequest(BaseModel):
    date_string: str
    start_time: str

    @field_validator("date_string")
    @classmethod
    def validate_date(cls, value: str) -> str:
        parsed_date = datetime.strptime(value, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%Y-%m-%d")

        if formatted_date != value:
            raise ValueError("Invalid date format")

        return value

    @field_validator("start_time")
    @classmethod
    def validate_time(cls, value: str) -> str:
        parsed_time = datetime.strptime(value, "%H:%M").time()
        formatted_time = parsed_time.strftime("%H:%M")

        if formatted_time != value:
            raise ValueError("Invalid time format")

        return value

@app.post("/validate")
def read(request: ScheduleRequest):
    try:
        return {"valid": validate_schedule(request.date_string, request.start_time)}
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date or time")