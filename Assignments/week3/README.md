# Music Playlist Manager (Week 03 Assignment)

A web-based application to manage and sort music playlists using various sorting algorithms. This project compares the performance of Selection Sort, Insertion Sort, and Merge Sort.

## Features
- **Random Playlist Generation**: Generate a playlist of N songs.
- **Sorting Algorithms**: Implements Selection Sort ($O(n^2)$), Insertion Sort ($O(n^2)$), and Merge Sort ($O(n \log n)$).
- **Multiple Criteria**: Sort by Title, Artist, Duration, or Play Count.
- **Performance Analysis**: Displays comparisons, swaps, and execution time for each sort.
- **Algorithm Comparison**: A "Compare All" feature to run all algorithms simultaneously for benchmarking.

## Prerequisites
- Python 3.7+
- Pip (Python package manager)

## Installation

1. Navigate to the project directory:
   ```bash
   cd Assignments/week3
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   python app.py
   ```

2. Open your web browser and go to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Project Structure
- `app.py`: Backend server logic and sorting algorithm implementations.
- `static/`: Frontend assets (HTML, CSS, JavaScript).
- `requirements.txt`: Python dependencies.
- `REPORT.md`: Detailed performance analysis and assignment report.
