# Assignment 01: Complexity Analysis & Performance Report

**Course:** 2026 Algorithm Lecture (Korea Univ. 26-1)  
**Topic:** Empirical Validation of Time Complexity (O(1), O(n), O(n²))  
**Student ID / Name:** OhSeJun  
**Date:** March 16, 2026

---

## 1. Experimental Setup & Implementation

We implemented three search strategies within a FastAPI backend to observe their performance characteristics under load.

### A. Search Strategies
- **ID Lookup ($O(1)$):** Uses a pre-populated Python dictionary. Retrieval time is independent of the dataset size.
- **Name Search ($O(n)$):** Scans the list of 1,000 products once using a list comprehension.
- **Duplicate Detection ($O(n^2)$):** Employs nested loops to compare every product pair ($N \times N$) to identify duplicate names.

### B. Screenshot Evidence (Search Results)

![ID Search Result](.images/locust_search_id.png)
<div class="caption">Figure 1: O(1) Search result showing constant-time response (minimal latency).</div>

![Name Search Result](.images/locust_search_name.png)
<div class="caption">Figure 2: O(n) Search result showing linear scanning of the product list.</div>

![Duplicate Search Result](.images/locust_search_duplicates.png)
<div class="caption">Figure 3: O(n²) Search result showing significantly higher latency for the same dataset.</div>

---

## 2. Performance Evaluation (Locust Load Test)

We simulated up to **50 concurrent users** using Locust to evaluate how the server handles stress across different complexities.

### A. Load Test Execution
![Locust Main](.images/locust_main.png)
<div class="caption">Figure 4: Locust load test configuration (50 concurrent users).</div>

### B. Statistical Results

| Search Type | Complexity | Avg Response Time (ms) | Max Response Time (ms) |
| :--- | :---: | :---: | :---: |
| **ID Lookup** | $O(1)$ | **~1 ms** | **~5 ms** |
| **Name Search** | $O(n)$ | **~3 ms** | **~12 ms** |
| **Duplicate Search** | $O(n^2)$ | **~25 ms** | **~150+ ms** |

![Locust Statistics](.images/locust_statistics.png)
<div class="caption">Figure 5: Detailed performance statistics by endpoint.</div>

### C. Scalability Chart
![Locust Chart](.images/locust_chart.png)
<div class="caption">Figure 6: Response time chart showing exponential degradation for O(n²).</div>

---

## 3. Analysis: Why $O(n^2)$ Degrades Under Load

The performance gap between $O(1)$ and $O(n^2)$ is not just mathematical but has significant real-world implications:

1.  **Quadratic Growth:** With 1,000 items, $O(n)$ performs 1,000 operations, while $O(n^2)$ performs **1,000,000 operations**. When 50 users request this simultaneously, the CPU must handle 50 million operations, leading to a bottleneck.
2.  **CPU Starvation:** $O(n^2)$ logic consumes nearly 100% of a CPU core during execution. Under high concurrency, requests are queued because the CPU cannot clear previous tasks fast enough, causing "Tail Latency" to skyrocket.
3.  **Real-World Impact:** As seen in Figure 6, while $O(1)$ and $O(n)$ remain stable, the $O(n^2)$ response time (yellow/green lines) spikes as user count grows, eventually leading to timeouts and a degraded user experience.

---

## 4. Conclusion

The results empirically prove that $O(n^2)$ algorithms are the primary cause of system instability in high-traffic environments. To optimize, a **Hash-based approach** (using a set for duplicate checking) should be used to reduce the complexity to $O(n)$, ensuring system reliability even under extreme load.

---
*End of Report*
