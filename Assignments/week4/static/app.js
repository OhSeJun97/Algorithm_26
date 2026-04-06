document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const generateBtn = document.getElementById('generate-btn');
    const findBtn = document.getElementById('find-btn');
    const pointCountInput = document.getElementById('point-count');
    
    const bfTime = document.getElementById('bf-time');
    const bfDist = document.getElementById('bf-dist');
    const dcTime = document.getElementById('dc-time');
    const dcDist = document.getElementById('dc-dist');
    const speedup = document.getElementById('speedup');

    let currentPoints = [];

    function drawPoints(points, highlightPair = null) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw all points
        ctx.fillStyle = '#4a5568';
        points.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
            ctx.fill();
        });

        // Draw closest pair
        if (highlightPair) {
            const [p1, p2] = highlightPair;
            
            ctx.strokeStyle = '#e53e3e';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();

            ctx.fillStyle = '#e53e3e';
            [p1, p2].forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
                ctx.fill();
            });
        }
    }

    generateBtn.addEventListener('click', async () => {
        const n = parseInt(pointCountInput.value);
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ n })
            });
            const data = await response.json();
            currentPoints = data.points;
            drawPoints(currentPoints);
            findBtn.disabled = false;
            
            // Reset labels
            bfTime.textContent = 'Execution Time: - ms';
            bfDist.textContent = 'Min Distance: -';
            dcTime.textContent = 'Execution Time: - ms';
            dcDist.textContent = 'Min Distance: -';
            speedup.textContent = 'Speedup Ratio: -x';
        } catch (err) {
            console.error('Error generating points:', err);
        }
    });

    findBtn.addEventListener('click', async () => {
        if (currentPoints.length < 2) return;
        
        try {
            const response = await fetch('/closest-pair', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentPoints)
            });
            const data = await response.json();
            
            const bf = data.brute_force;
            const dc = data.divide_conquer;
            
            bfTime.textContent = `Execution Time: ${bf.time_ms.toFixed(4)} ms`;
            bfDist.textContent = `Min Distance: ${bf.distance.toFixed(4)}`;
            
            dcTime.textContent = `Execution Time: ${dc.time_ms.toFixed(4)} ms`;
            dcDist.textContent = `Min Distance: ${dc.distance.toFixed(4)}`;
            
            if (dc.time_ms > 0) {
                const ratio = bf.time_ms / dc.time_ms;
                speedup.textContent = `Speedup Ratio: ${ratio.toFixed(2)}x`;
            }
            
            drawPoints(currentPoints, dc.pair);
        } catch (err) {
            console.error('Error finding closest pair:', err);
        }
    });
});
