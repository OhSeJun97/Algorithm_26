from fastapi import FastAPI, Query, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import time
import random
import math

app = FastAPI()

class Point(BaseModel):
    x: float
    y: float

def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# 1. Brute Force O(n^2)
def brute_force(pts: List[Point]):
    min_d = float('inf')
    pair = None
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(pts[i], pts[j])
            if d < min_d:
                min_d = d
                pair = (pts[i], pts[j])
    return min_d, pair

# 2. Divide & Conquer O(n log^2 n)
def strip_closest(strip: List[Point], d, current_min_pair):
    min_d = d
    pair = current_min_pair
    # Sort by y-coordinate
    strip.sort(key=lambda p: p.y)
    
    n = len(strip)
    for i in range(n):
        # Only need to check the next few points in the y-sorted list
        for j in range(i + 1, n):
            if (strip[j].y - strip[i].y) >= min_d:
                break
            d_val = dist(strip[i], strip[j])
            if d_val < min_d:
                min_d = d_val
                pair = (strip[i], strip[j])
    return min_d, pair

def closest_pair_recursive(pts_sorted_x: List[Point]):
    n = len(pts_sorted_x)
    if n <= 3:
        return brute_force(pts_sorted_x)
    
    mid = n // 2
    mid_point = pts_sorted_x[mid]
    
    dl, pair_l = closest_pair_recursive(pts_sorted_x[:mid])
    dr, pair_r = closest_pair_recursive(pts_sorted_x[mid:])
    
    if dl < dr:
        d = dl
        min_pair = pair_l
    else:
        d = dr
        min_pair = pair_r
        
    strip = [p for p in pts_sorted_x if abs(p.x - mid_point.x) < d]
    d_strip, pair_strip = strip_closest(strip, d, min_pair)
    
    return d_strip, pair_strip

@app.post("/generate")
async def generate_points(n: int = Body(..., embed=True)):
    # Generate random points in a 800x600 canvas
    points = [Point(x=random.uniform(20, 780), y=random.uniform(20, 580)) for _ in range(n)]
    return {"points": points}

@app.post("/closest-pair")
async def find_closest_pair(points: List[Point] = Body(...)):
    # 1. Brute Force Timing
    start_bf = time.perf_counter()
    dist_bf, pair_bf = brute_force(points)
    end_bf = time.perf_counter()
    
    # 2. Divide & Conquer Timing
    start_dc = time.perf_counter()
    pts_sorted_x = sorted(points, key=lambda p: p.x)
    dist_dc, pair_dc = closest_pair_recursive(pts_sorted_x)
    end_dc = time.perf_counter()
    
    return {
        "brute_force": {
            "distance": dist_bf,
            "pair": pair_bf,
            "time_ms": (end_bf - start_bf) * 1000
        },
        "divide_conquer": {
            "distance": dist_dc,
            "pair": pair_dc,
            "time_ms": (end_dc - start_dc) * 1000
        }
    }

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
