
import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="CareFlow API",
    description="Event log and process analysis API",
    version="1.0.0",
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "sample_event_log.csv"


def read_events():
    if not CSV_FILE.is_file():
        raise HTTPException(
            status_code=404,
            detail="Sample event log file not found",
        )

    with CSV_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(
            line for line in file if line.strip()
        )

        if not reader.fieldnames or "case_id" not in reader.fieldnames:
            raise HTTPException(
                status_code=400,
                detail="CSV header is missing or invalid",
            )

        return list(reader)


@app.get("/")
def root():
    return {
        "message": "CareFlow backend is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/events")
def get_events():
    events = read_events()

    return {
        "total_events": len(events),
        "events": events,
    }


@app.get("/cases/{case_id}")
def get_case_events(case_id: str):
    events = read_events()

    case_events = [
        event
        for event in events
        if event.get("case_id") == case_id
    ]

    if not case_events:
        raise HTTPException(
            status_code=404,
            detail=f"No events found for case {case_id}",
        )

    return {
        "case_id": case_id,
        "total_events": len(case_events),
        "events": case_events,
    }
