from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import time
import copy
from typing import List, Optional

import os

app = FastAPI()

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class Song(BaseModel):
    id: int
    title: str
    artist: str
    duration: int  # in seconds
    play_count: int

class SortRequest(BaseModel):
    songs: List[Song]
    criterion: str  # title, artist, duration, play_count
    algorithm: str  # selection, insertion, merge

class CompareRequest(BaseModel):
    songs: List[Song]
    criterion: str

# In-memory storage for simplicity
current_playlist = []

def generate_random_song(song_id: int):
    titles = ["Song A", "Song B", "Song C", "Song D", "Song E", "Song F", "Song G", "Song H", "Song I", "Song J"]
    artists = ["Artist X", "Artist Y", "Artist Z", "Artist W", "Artist V"]
    return {
        "id": song_id,
        "title": f"{random.choice(titles)} {song_id}",
        "artist": random.choice(artists),
        "duration": random.randint(120, 300),
        "play_count": random.randint(0, 1000)
    }

# Sorting Algorithms
def selection_sort(arr, criterion):
    n = len(arr)
    comparisons = 0
    swaps = 0
    start_time = time.perf_counter()
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j][criterion] < arr[min_idx][criterion]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            
    end_time = time.perf_counter()
    return arr, comparisons, swaps, (end_time - start_time) * 1000

def insertion_sort(arr, criterion):
    n = len(arr)
    comparisons = 0
    swaps = 0
    start_time = time.perf_counter()
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j][criterion] > key[criterion]:
                arr[j+1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j+1] = key
        
    end_time = time.perf_counter()
    return arr, comparisons, swaps, (end_time - start_time) * 1000

def merge_sort_recursive(arr, criterion):
    comparisons = 0
    swaps = 0
    
    if len(arr) <= 1:
        return arr, 0, 0
    
    mid = len(arr) // 2
    left, c1, s1 = merge_sort_recursive(arr[:mid], criterion)
    right, c2, s2 = merge_sort_recursive(arr[mid:], criterion)
    
    comparisons += c1 + c2
    swaps += s1 + s2
    
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i][criterion] <= right[j][criterion]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            swaps += 1 # In merge sort, this is more like a move, but we'll count it for comparison
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged, comparisons, swaps

def merge_sort(arr, criterion):
    start_time = time.perf_counter()
    sorted_arr, comparisons, swaps = merge_sort_recursive(arr, criterion)
    end_time = time.perf_counter()
    return sorted_arr, comparisons, swaps, (end_time - start_time) * 1000

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(STATIC_DIR, "index.html")) as f:
        return f.read()

@app.post("/generate")
async def generate_playlist(count: int = 10):
    global current_playlist
    current_playlist = [generate_random_song(i) for i in range(count)]
    return current_playlist

@app.post("/sort")
async def sort_playlist(request: SortRequest):
    songs_data = [s.dict() for s in request.songs]
    if request.algorithm == "selection":
        sorted_songs, comp, swaps, exec_time = selection_sort(songs_data, request.criterion)
    elif request.algorithm == "insertion":
        sorted_songs, comp, swaps, exec_time = insertion_sort(songs_data, request.criterion)
    elif request.algorithm == "merge":
        sorted_songs, comp, swaps, exec_time = merge_sort(songs_data, request.criterion)
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid algorithm"})
    
    return {
        "songs": sorted_songs,
        "comparisons": comp,
        "swaps": swaps,
        "execution_time_ms": exec_time
    }

@app.post("/compare")
async def compare_all(request: CompareRequest):
    songs_data = [s.dict() for s in request.songs]
    results = {}
    
    # Selection Sort
    _, comp, swaps, exec_time = selection_sort(copy.deepcopy(songs_data), request.criterion)
    results["selection"] = {"comparisons": comp, "swaps": swaps, "execution_time_ms": exec_time}
    
    # Insertion Sort
    _, comp, swaps, exec_time = insertion_sort(copy.deepcopy(songs_data), request.criterion)
    results["insertion"] = {"comparisons": comp, "swaps": swaps, "execution_time_ms": exec_time}
    
    # Merge Sort
    _, comp, swaps, exec_time = merge_sort(copy.deepcopy(songs_data), request.criterion)
    results["merge"] = {"comparisons": comp, "swaps": swaps, "execution_time_ms": exec_time}
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
