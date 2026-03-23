let currentSongs = [];

document.getElementById('generateBtn').addEventListener('click', async () => {
    const count = document.getElementById('songCount').value;
    const response = await fetch(`/generate?count=${count}`, { method: 'POST' });
    currentSongs = await response.json();
    updateTable(currentSongs);
    document.getElementById('stats').style.display = 'none';
    document.getElementById('comparisonTableContainer').style.display = 'none';
});

document.getElementById('sortBtn').addEventListener('click', async () => {
    if (currentSongs.length === 0) {
        alert("Generate a playlist first!");
        return;
    }

    const criterion = document.getElementById('criterion').value;
    const algorithm = document.getElementById('algorithm').value;

    const response = await fetch('/sort', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            songs: currentSongs,
            criterion: criterion,
            algorithm: algorithm
        })
    });

    const result = await response.json();
    currentSongs = result.songs;
    updateTable(currentSongs);
    showStats(algorithm, result);
});

document.getElementById('compareBtn').addEventListener('click', async () => {
    if (currentSongs.length === 0) {
        alert("Generate a playlist first!");
        return;
    }

    const criterion = document.getElementById('criterion').value;

    const response = await fetch('/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            songs: currentSongs,
            criterion: criterion
        })
    });

    const results = await response.json();
    showComparison(results);
});

function updateTable(songs) {
    const body = document.getElementById('playlistBody');
    let htmlContent = '';
    songs.forEach(song => {
        htmlContent += `<tr>
            <td>${song.id}</td>
            <td>${song.title}</td>
            <td>${song.artist}</td>
            <td>${song.duration}</td>
            <td>${song.play_count}</td>
        </tr>`;
    });
    body.innerHTML = htmlContent;
}

function showStats(algo, result) {
    document.getElementById('stats').style.display = 'block';
    document.getElementById('resAlgo').innerText = algo.charAt(0).toUpperCase() + algo.slice(1);
    document.getElementById('resComp').innerText = result.comparisons;
    document.getElementById('resSwaps').innerText = result.swaps;
    document.getElementById('resTime').innerText = result.execution_time_ms.toFixed(4);
}

function showComparison(results) {
    document.getElementById('comparisonTableContainer').style.display = 'block';
    const body = document.getElementById('comparisonBody');
    body.innerHTML = '';
    
    for (const [algo, data] of Object.entries(results)) {
        const row = `<tr>
            <td>${algo.charAt(0).toUpperCase() + algo.slice(1)} Sort</td>
            <td>${data.comparisons}</td>
            <td>${data.swaps}</td>
            <td>${data.execution_time_ms.toFixed(4)}</td>
        </tr>`;
        body.innerHTML += row;
    }
}
