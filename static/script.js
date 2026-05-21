let currentClimate = { ac: { active: false }, floor: { active: false } };
let vacuumState = { state: "idling", fan_power: 102, water_level: 201 };

const fanModes = { 101: "Quiet", 102: "Balanced", 103: "Turbo", 104: "Max" };
const waterModes = { 200: "Off", 201: "Low", 202: "Medium", 203: "High" };

function updateInterface() {
    fetch('/api/status')
        .then(r => r.json())
        .then(data => {

            const homeStatusEl = document.getElementById('home-status');
            if (homeStatusEl) {
                homeStatusEl.innerText = data.anyone_home ? "Вдома є люди" : "Вдома нікого немає";
                homeStatusEl.style.color = data.anyone_home ? "#4CAF50" : "#f44336";
            }
            if (document.getElementById('users-display')) {
                document.getElementById('users-display').innerHTML = data.active_users.map(n => `<span class="user-tag">${n}</span>`).join('');
            }

            for (let r in data.lights) {
                const el = document.getElementById(r);
                if (el) el.className = data.lights[r] ? 'card active' : 'card';
            }
            const fanEl = document.getElementById('Toilet_Fan_Card');
            if (fanEl) fanEl.className = data.fans.Toilet_Fan ? 'card active' : 'card';

            if (data.climate) {
                currentClimate = data.climate;
                ['floor', 'ac'].forEach(dev => {
                    const item = data.climate[dev];
                    if (!item) return;

                    const valEl = document.getElementById(`${dev}-val`);
                    const sliderEl = document.getElementById(`slider-${dev}`);
                    const btnEl = document.getElementById(`btn-${dev}`);
                    const statusText = document.getElementById(`${dev}-status-text`);

                    if (valEl) valEl.innerText = item.val;
                    if (sliderEl) {
                        sliderEl.value = item.val;
                        sliderEl.disabled = !item.active;
                    }
                    if (btnEl) {
                        btnEl.innerText = item.active ? "ON" : "OFF";
                        btnEl.className = item.active ? "btn-toggle on" : "btn-toggle";
                    }
                    if (statusText) {
                        statusText.innerText = `Кондиціонер: ${item.active ? "ON" : "OFF"}`;
                    }

                    if (dev === 'ac' && item.mode) {
                        ['cool', 'heat', 'dry'].forEach(m => {
                            const mBtn = document.getElementById(`mode-${m}`);
                            if (mBtn) {
                                if (item.mode === m) mBtn.classList.add('active');
                                else mBtn.classList.remove('active');
                            }
                        });
                    }
                });
            }

            if (data.vacuum) {
                vacuumState = data.vacuum;
                const statusEl = document.getElementById('vac-status-display');
                if (statusEl) statusEl.innerText = vacuumState.state.toUpperCase();
                
                const mainBtn = document.getElementById('vac-main-btn');
                if (mainBtn) {
                    mainBtn.innerText = vacuumState.state === "cleaning" ? "Стоп" : "Прибрати";
                    if (vacuumState.state === "cleaning") mainBtn.classList.add('vac-active');
                    else mainBtn.classList.remove('vac-active');
                }

                const homeBtn = document.getElementById('vac-home');
                if (homeBtn) {
                    if (["returning", "charging"].includes(vacuumState.state)) homeBtn.classList.add('vac-active');
                    else homeBtn.classList.remove('vac-active');
                }

                if (document.getElementById('vac-fan-val')) 
                    document.getElementById('vac-fan-val').innerText = fanModes[vacuumState.fan_power] || "Unknown";
                if (document.getElementById('slider-vac-fan')) 
                    document.getElementById('slider-vac-fan').value = vacuumState.fan_power;
            }
        })
        .catch(err => console.error("Помилка оновлення:", err));
}

function toggleClimate(dev) {
    const isNowActive = currentClimate[dev] ? currentClimate[dev].active : false;
    fetch('/set_climate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({device: dev, active: !isNowActive})
    }).then(() => updateInterface());
}

function toggleAC() {
    toggleClimate('ac');
}

function sendACParam(type, val) {
    fetch('/api/ac/params', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ type: type, value: val })
    }).then(r => { if(r.ok) updateInterface(); });
}

function handleVacuumMainAction() {
    controlVacuum(vacuumState.state === "cleaning" ? 'stop' : 'start');
}

function controlVacuum(cmd) {
    fetch(`/api/vacuum/command/${cmd}`, { method: 'POST' }).then(() => updateInterface());
}

function sendVacParam(type, val) {
    fetch('/api/vacuum/params', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ type: type, value: parseInt(val) })
    }).then(() => updateInterface());
}

function updateVacLabels(type, val) {
    const labelId = type === 'fan' ? 'vac-fan-val' : 'vac-water-val';
    const dict = type === 'fan' ? fanModes : waterModes;
    if (document.getElementById(labelId)) document.getElementById(labelId).innerText = dict[val];
}

function toggleLight(room) { fetch(`/toggle/${room}`).then(() => updateInterface()); }
function toggleFan(fan) { fetch(`/toggle_fan/${fan}`).then(() => updateInterface()); }

setInterval(updateInterface, 1000);
updateInterface();