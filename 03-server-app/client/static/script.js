document.getElementById('trayectoForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const trayecto = document.getElementById('trayecto').value;
    const statusMessage = document.getElementById('statusMessage');

    try {
        const response = await fetch('/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ trayecto: trayecto })
        });

        if (response.ok) {
            const result = await response.json();
            statusMessage.textContent = `Trayecto iniciado: ${trayecto}`;
            statusMessage.style.color = 'green';
        } else {
            const error = await response.json();
            statusMessage.textContent = `Error: ${error.error}`;
            statusMessage.style.color = 'red';
        }
    } catch (err) {
        statusMessage.textContent = `Error al iniciar el trayecto: ${err.message}`;
        statusMessage.style.color = 'red';
    }
});
