function updateAllStatuses() {
    fetch('/api/status')
        .then(response => response.json())
        .then(state => {
            console.log("Отримано стан будинку:", state);
            
            let lighting = state.lighting;
            for (let room in lighting) {
                let button = document.getElementById('btn-' + room);
                if (button) {
                    if (lighting[room] === 1) button.classList.add('active');
                    else button.classList.remove('active');
                }
            }

            let fanButton = document.getElementById('btn-ventilation');
            if (fanButton) {
                if (state.ventilation === 1) fanButton.classList.add('active');
                else fanButton.classList.remove('active');
            }

            let acButton = document.getElementById('btn-ac');
            if (acButton) {
                if (state.ac.is_on) acButton.classList.add('active');
                else acButton.classList.remove('active');
            }
            document.getElementById('range-ac').value = state.ac.temperature;
            document.getElementById('val-ac').innerText = state.ac.temperature + "°C";
            document.getElementById('select-ac-mode').value = state.ac.mode;
            document.getElementById('select-ac-fan').value = state.ac.fan_speed;
            document.getElementById('select-ac-swing').value = state.ac.swing;

            let floorButton = document.getElementById('btn-floor');
            if (floorButton) {
                if (state.climate.state === 1) floorButton.classList.add('active');
                else floorButton.classList.remove('active');
            }
            document.getElementById('range-floor').value = state.climate.power;
            document.getElementById('val-floor').innerText = state.climate.power + "%";

            let vacStateText = {
                "idle": "В очікуванні 💤",
                "cleaning": "Прибирає 🧹",
                "returning": "Повертається 🏠",
                "charging": "Заряджається ⚡",
                "paused": "На паузі ⏸️"
            };
            document.getElementById('val-vacuum-state').innerText = vacStateText[state.vacuum.state] || state.vacuum.state;
            
            document.getElementById('select-vac-fan').value = state.vacuum.fan_power;
            document.getElementById('select-vac-water').value = state.vacuum.water_level;
        })
        .catch(error => console.error("Помилка синхронізації:", error));
}

window.addEventListener('DOMContentLoaded', updateAllStatuses);

function toggleLight(room) {
    fetch('/toggle/' + room).then(response => response.json()).then(data => {
        let button = document.getElementById('btn-' + room);
        if (button) {
            if (data.new_state === 1) button.classList.add('active');
            else button.classList.remove('active');
        }
    });
}

function toggleFan() {
    fetch('/toggle_fan').then(response => response.json()).then(data => {
        let button = document.getElementById('btn-ventilation');
        if (button) {
            if (data.new_fan_state === 1) button.classList.add('active');
            else button.classList.remove('active');
        }
    });
}

function changeACTemp(val) {
    document.getElementById('val-ac').innerText = val + "°C";
    fetch('/set_climate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ device: "ac", value: val })
    });
}

function toggleAC() {
    let button = document.getElementById('btn-ac');
    let isActivating = !button.classList.contains('active');
    button.classList.toggle('active');
    fetch('/set_climate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ device: "ac", active: isActivating })
    });
}

function changeACParam(paramType, paramValue) {
    fetch('/api/ac/params', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ type: paramType, value: paramValue })
    });
}

function changeFloorPower(val) {
    document.getElementById('val-floor').innerText = val + "%";
    fetch('/set_climate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ device: "floor", value: val })
    });
}

function sendVacuumCmd(cmd) {
    console.log("Команда пилососу:", cmd);
    fetch('/api/vacuum/command/' + cmd)
        .then(response => response.json())
        .then(data => {
            updateAllStatuses();
        });
}

function changeVacParam(paramType, paramValue) {
    console.log(`Параметр пилососа [${paramType}]: ${paramValue}`);
    fetch('/api/vacuum/params', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ type: paramType, value: paramValue })
    });
}

function toggleFloor() {
    let button = document.getElementById('btn-floor');
    let isActivating = !button.classList.contains('active');
    button.classList.toggle('active');
    fetch('/set_climate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ device: "floor", active: isActivating })
    });
}

setInterval(updateAllStatuses, 1000);