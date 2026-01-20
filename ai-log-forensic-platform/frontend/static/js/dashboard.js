/* =========================================================
   AI LOG FORENSIC PLATFORM – DASHBOARD JS (FINAL)
========================================================= */

/* =========================================================
   LOGIN FUNCTION (IMPORTANT)
========================================================= */
function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const error = document.getElementById("error");

    fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(res => {
        if (res.status === 200) {
            window.location.href = "/dashboard";
        } else {
            error.innerText = "Invalid username or password";
        }
    })
    .catch(() => {
        error.innerText = "Server error";
    });
}

/* =========================================================
   LOAD DASHBOARD DATA
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname === "/dashboard") {
        loadStats();
        loadSystems();
        loadAlerts();

        // Auto refresh every 10 seconds
        setInterval(() => {
            loadStats();
            loadSystems();
            loadAlerts();
        }, 10000);
    }
});

/* =========================================================
   LOAD DASHBOARD STATS
========================================================= */
function loadStats() {
    fetch("/dashboard/stats")
        .then(res => res.json())
        .then(data => {
            setText("total-systems", data.total_systems || 0);
            setText("total-logs", data.total_logs || 0);
            setText("total-alerts", data.total_alerts || 0);
        })
        .catch(() => console.warn("Stats load failed"));
}

/* =========================================================
   LOAD SYSTEMS
========================================================= */
function loadSystems() {
    const table = document.getElementById("systems-table");
    if (!table) return;

    table.innerHTML = "";

    fetch("/dashboard/systems")
        .then(res => res.json())
        .then(systems => {
            if (!systems.length) {
                const row = table.insertRow();
                row.insertCell(0).innerText = "No systems registered";
                row.insertCell(1).innerText = "-";
                row.insertCell(2).innerText = "-";
                row.insertCell(3).innerText = "-";
                return;
            }

            systems.forEach(sys => {
                const row = table.insertRow();
                row.insertCell(0).innerText = sys.system_id;
                row.insertCell(1).innerText = sys.hostname;
                row.insertCell(2).innerText = sys.last_seen || "N/A";

                const statusCell = row.insertCell(3);
                statusCell.innerHTML = sys.last_seen
                    ? '<span class="online">ONLINE</span>'
                    : '<span class="offline">OFFLINE</span>';
            });
        })
        .catch(() => console.warn("Systems load failed"));
}

/* =========================================================
   LOAD ALERTS
========================================================= */
function loadAlerts() {
    const table = document.getElementById("alerts-table");
    if (!table) return;

    table.innerHTML = "";

    fetch("/dashboard/alerts")
        .then(res => res.json())
        .then(alerts => {
            if (!alerts.length) {
                const row = table.insertRow();
                row.insertCell(0).innerText = "No alerts detected";
                row.insertCell(1).innerText = "-";
                row.insertCell(2).innerText = "-";
                return;
            }

            alerts.forEach(alert => {
                const row = table.insertRow();
                row.insertCell(0).innerText = alert.system_id;
                row.insertCell(1).innerText = alert.description;
                row.insertCell(2).innerText = alert.created_at;
            });
        })
        .catch(() => console.warn("Alerts load failed"));
}

/* =========================================================
   HELPER FUNCTION
========================================================= */
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerText = value;
}
