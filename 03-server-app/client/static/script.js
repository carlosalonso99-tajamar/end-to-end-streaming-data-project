document.getElementById('trayectoForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const trayecto = document.getElementById('trayecto').value;

    const response = await fetch('/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trayecto: trayecto })
    });

    const result = await response.json();
    const responseDiv = document.getElementById('response');
    responseDiv.textContent = JSON.stringify(result, null, 2);
});
