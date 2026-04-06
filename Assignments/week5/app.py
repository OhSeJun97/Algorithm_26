from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

class Reservation(BaseModel):
    id: int
    name: str
    start: float
    end: float

# Greedy Activity Selection Algorithm
def select_activities(activities: List[Reservation]):
    # 1. Sort by finish time
    sorted_activities = sorted(activities, key=lambda x: x.end)
    
    selected = []
    trace = []
    
    if not sorted_activities:
        return selected, trace
    
    # 2. Greedily select non-overlapping events
    last_end_time = 0
    for activity in sorted_activities:
        if activity.start >= last_end_time:
            selected.append(activity)
            last_end_time = activity.end
            trace.append({
                "activity": activity,
                "status": "Selected",
                "reason": f"Starts at {activity.start} >= last finish time {last_end_time - (activity.end - activity.start)}"
            })
        else:
            trace.append({
                "activity": activity,
                "status": "Rejected",
                "reason": f"Starts at {activity.start} < last finish time {last_end_time}"
            })
            
    return selected, trace

@app.post("/generate")
async def generate_reservations(n: int = Body(..., embed=True)):
    reservations = []
    event_names = ["Algorithm", "OS", "DB", "AI", "Network", "Security", "Web", "Graphics", "Compiler", "Architecture", "Discrete Math", "Software Eng", "Logic Design", "Circuit", "Signal"]
    
    for i in range(n):
        # Generate random start time between 9:00 and 17:00 (9 to 17)
        start = round(random.uniform(9, 16.5), 1)
        # Duration between 0.5 and 2.5 hours
        duration = round(random.uniform(0.5, 2.5), 1)
        end = round(start + duration, 1)
        if end > 18: end = 18 # Limit to 6 PM
        
        reservations.append(Reservation(
            id=i,
            name=f"{random.choice(event_names)} {i+1}",
            start=start,
            end=end
        ))
    return {"reservations": reservations}

@app.post("/schedule")
async def schedule_activities(reservations: List[Reservation] = Body(...)):
    selected, trace = select_activities(reservations)
    return {
        "selected": selected,
        "trace": trace,
        "total_requests": len(reservations),
        "selected_count": len(selected)
    }

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
