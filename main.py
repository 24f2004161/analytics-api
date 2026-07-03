from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_9vvvh79288u7pwe03c127vea"
EMAIL = "YOUR_EMAIL@example.com"

app = FastAPI()

# Allow browser access for the grader
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class EventBatch(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    batch: EventBatch,
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    revenue = 0.0
    totals = defaultdict(float)

    for event in batch.events:
        if event.amount > 0:
            revenue += event.amount
            totals[event.user] += event.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": len(batch.events),
        "unique_users": len({e.user for e in batch.events}),
        "revenue": revenue,
        "top_user": top_user,
    }
