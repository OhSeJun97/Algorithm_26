document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const addBtn = document.getElementById('add-btn');
    const genBtn = document.getElementById('gen-btn');
    const clearBtn = document.getElementById('clear-btn');
    const scheduleBtn = document.getElementById('schedule-btn');
    
    const resName = document.getElementById('res-name');
    const resStart = document.getElementById('res-start');
    const resEnd = document.getElementById('res-end');
    const genCount = document.getElementById('gen-count');
    
    const statsBox = document.getElementById('stats-box');
    const selectedCount = document.getElementById('selected-count');
    const totalCount = document.getElementById('total-count');
    const traceList = document.getElementById('trace-list');

    let reservations = [];
    let selectedIds = new Set();

    function drawTimeline() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw grid lines for hours 9 to 18
        const startHour = 9;
        const endHour = 18;
        const totalWidth = canvas.width - 60;
        const xOffset = 40;
        
        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 1;
        ctx.fillStyle = '#64748b';
        ctx.font = '10px sans-serif';
        
        for (let h = startHour; h <= endHour; h++) {
            const x = xOffset + ((h - startHour) / (endHour - startHour)) * totalWidth;
            ctx.beginPath();
            ctx.moveTo(x, 30);
            ctx.lineTo(x, canvas.height - 30);
            ctx.stroke();
            ctx.fillText(`${h}:00`, x - 15, canvas.height - 15);
        }

        if (reservations.length === 0) return;

        // Draw activities
        const rowHeight = 25;
        const startY = 40;
        
        reservations.forEach((res, index) => {
            const xStart = xOffset + ((res.start - startHour) / (endHour - startHour)) * totalWidth;
            const xEnd = xOffset + ((res.end - startHour) / (endHour - startHour)) * totalWidth;
            const y = startY + (index % 12) * rowHeight; // Reuse rows every 12 items
            
            const isSelected = selectedIds.has(res.id);
            ctx.fillStyle = isSelected ? '#10b981' : '#cbd5e0';
            
            // Bar
            ctx.beginPath();
            ctx.roundRect(xStart, y, xEnd - xStart, 18, 4);
            ctx.fill();
            
            // Text
            ctx.fillStyle = isSelected ? 'white' : '#475569';
            ctx.font = 'bold 9px sans-serif';
            ctx.fillText(res.name, xStart + 4, y + 12);
        });
    }

    addBtn.addEventListener('click', () => {
        const name = resName.value || "Custom Event";
        const start = parseFloat(resStart.value);
        const end = parseFloat(resEnd.value);
        
        if (isNaN(start) || isNaN(end) || start >= end) {
            alert("Please enter valid start/end times.");
            return;
        }
        
        reservations.push({ id: Date.now(), name, start, end });
        drawTimeline();
        resName.value = ''; resStart.value = ''; resEnd.value = '';
    });

    genBtn.addEventListener('click', async () => {
        const n = parseInt(genCount.value);
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ n })
        });
        const data = await response.json();
        reservations = data.reservations;
        selectedIds.clear();
        statsBox.style.display = 'none';
        traceList.innerHTML = '<p class="empty-text">No data to display. Run schedule first.</p>';
        drawTimeline();
    });

    clearBtn.addEventListener('click', () => {
        reservations = [];
        selectedIds.clear();
        statsBox.style.display = 'none';
        traceList.innerHTML = '<p class="empty-text">No data to display. Run schedule first.</p>';
        drawTimeline();
    });

    scheduleBtn.addEventListener('click', async () => {
        if (reservations.length === 0) return;
        
        const response = await fetch('/schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reservations)
        });
        const data = await response.json();
        
        selectedIds = new Set(data.selected.map(r => r.id));
        selectedCount.textContent = data.selected_count;
        totalCount.textContent = data.total_requests;
        statsBox.style.display = 'block';
        
        // Update Trace List
        traceList.innerHTML = '';
        data.trace.forEach(item => {
            const div = document.createElement('div');
            div.className = `trace-item ${item.status}`;
            div.innerHTML = `
                <div><span class="status-badge">${item.status}</span> <strong>${item.activity.name}</strong> (${item.activity.start} - ${item.activity.end})</div>
                <div style="margin-top:4px; opacity:0.8;">${item.reason}</div>
            `;
            traceList.appendChild(div);
        });
        
        drawTimeline();
    });

    drawTimeline();
});
