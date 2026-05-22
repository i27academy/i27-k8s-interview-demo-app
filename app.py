"""
i27Academy — Ultra-Premium SaaS Dashboard
Elevated with glassmorphism, atmospheric lighting, and high-end animations.
"""

from flask import Flask, jsonify, request, render_template_string
import os, sys, time, threading, logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [i27academy] %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "v1")
APP_ENV     = os.environ.get("APP_ENV", "production")
APP_COLOR   = os.environ.get("APP_COLOR", "orange")
EPISODE     = os.environ.get("EPISODE", "demo")
READY       = True
HEALTHY     = True
START_TIME  = time.time()

UI_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>i27Academy Demo App</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #f6f8fb;
  --card: #ffffff;
  --text: #111827;
  --muted: #667085;
  --line: #e4e7ec;
  --brand: #f15e22;
  --brand-dark: #c84a16;
  --navy: #101828;
  --green: #16803c;
  --red: #d92d20;
  --amber: #b54708;
  --blue: #175cd3;
  --shadow: 0 14px 34px rgba(16, 24, 40, 0.08);
  --font: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --mono: 'JetBrains Mono', Consolas, monospace;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
}
button { font: inherit; }

.page {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px 0 40px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.logo {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: grid;
  place-items: center;
  background: var(--brand);
  color: #fff;
  font-weight: 800;
  letter-spacing: 0;
  box-shadow: 0 10px 22px rgba(241, 94, 34, 0.24);
}

.brand-title {
  margin: 0;
  font-size: 26px;
  line-height: 1.1;
  font-weight: 800;
  letter-spacing: 0;
}
.brand-title .prefix { color: var(--brand); }
.brand-title .word { color: var(--navy); }
.brand-subtitle {
  margin: 5px 0 0;
  color: var(--muted);
  font-size: 14px;
}

.header-meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  color: var(--muted);
  font-size: 13px;
  font-weight: 600;
}
.chip strong { color: var(--text); }
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green);
}

.hero {
  background: var(--navy);
  color: #fff;
  border-radius: 8px;
  padding: 28px;
  box-shadow: var(--shadow);
  margin-bottom: 18px;
}
.hero h2 {
  margin: 0;
  font-size: 28px;
  line-height: 1.2;
  letter-spacing: 0;
}
.hero p {
  max-width: 740px;
  margin: 10px 0 0;
  color: #cbd5e1;
  line-height: 1.6;
}

.grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 18px;
  align-items: start;
}

.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
}
.card-header {
  padding: 18px 20px;
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}
.card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0;
}
.card-subtitle {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 13px;
}
.card-body { padding: 20px; }

.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}
.stat {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
  min-height: 110px;
}
.label {
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 800;
}
.value {
  margin-top: 10px;
  font-size: 22px;
  line-height: 1.2;
  font-weight: 800;
  overflow-wrap: anywhere;
}
.note {
  margin-top: 8px;
  color: var(--muted);
  font-size: 13px;
}

.probes {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.probe {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
  background: #fcfcfd;
}
.probe-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 14px;
}
.probe-name { font-weight: 800; }
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 800;
  border: 1px solid transparent;
  white-space: nowrap;
}
.badge.good { color: var(--green); background: #ecfdf3; border-color: #abefc6; }
.badge.bad { color: var(--red); background: #fef3f2; border-color: #fecdca; }
.badge.warn { color: var(--amber); background: #fffaeb; border-color: #fedf89; }
.bar {
  height: 8px;
  border-radius: 999px;
  background: #eaecf0;
  overflow: hidden;
}
.bar span {
  display: block;
  width: 0%;
  height: 100%;
  background: var(--green);
  border-radius: inherit;
  transition: width .2s ease, background .2s ease;
}

.details {
  width: 100%;
  border-collapse: collapse;
  margin-top: 18px;
}
.details th, .details td {
  padding: 13px 0;
  border-bottom: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}
.details th {
  width: 36%;
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.details td {
  font-weight: 700;
  overflow-wrap: anywhere;
}

.actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.action {
  min-height: 74px;
  padding: 13px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  color: var(--text);
  text-align: left;
  cursor: pointer;
  transition: border-color .15s ease, box-shadow .15s ease, transform .15s ease;
}
.action:hover {
  border-color: #b8c2d0;
  box-shadow: 0 10px 24px rgba(16, 24, 40, .08);
  transform: translateY(-1px);
}
.action strong { display: block; font-size: 14px; }
.action span {
  display: block;
  margin-top: 5px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 12px;
}
.action.warning { background: #fffbf5; border-color: #fedf89; }
.action.danger { background: #fff5f5; border-color: #fecdca; }

.log {
  min-height: 300px;
  max-height: 360px;
  overflow-y: auto;
  background: #111827;
  color: #e5e7eb;
  border-radius: 8px;
  padding: 14px;
  font-family: var(--mono);
  font-size: 12px;
  line-height: 1.65;
}
.log-entry { margin-bottom: 8px; }
.time { color: #9ca3af; margin-right: 7px; }
.type-info { color: #93c5fd; }
.type-warn { color: #fdba74; }
.type-error { color: #fca5a5; }

@media (max-width: 980px) {
  .header { align-items: flex-start; flex-direction: column; }
  .header-meta { justify-content: flex-start; }
  .grid { grid-template-columns: 1fr; }
  .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 620px) {
  .page { width: min(100% - 24px, 1180px); padding-top: 16px; }
  .hero { padding: 22px; }
  .hero h2 { font-size: 23px; }
  .stats, .probes, .actions { grid-template-columns: 1fr; }
  .brand-title { font-size: 23px; }
}
</style>
</head>
<body>
  <div class="page">
    <header class="header">
      <div class="brand">
        <div class="logo">i27</div>
        <div>
          <h1 class="brand-title"><span class="prefix">i27</span><span class="word">Academy</span></h1>
          <p class="brand-subtitle">Kubernetes interview demo application</p>
        </div>
      </div>
      <div class="header-meta">
        <span class="chip"><span class="dot" id="status-dot"></span><strong id="overall-status">Operational</strong></span>
        <span class="chip">Node <strong id="node">-</strong></span>
        <span class="chip">Env <strong id="env">-</strong></span>
      </div>
    </header>

    <section class="hero">
      <h2>Production-ready demo console 1</h2>
      <p>Monitor app metadata, probe status, runtime configuration, and failure simulation endpoints from a clean i27Academy interface.</p>
    </section>

    <section class="stats">
      <div class="stat"><div class="label">Version</div><div id="version" class="value">-</div><div class="note">Current release</div></div>
      <div class="stat"><div class="label">Episode</div><div id="episode" class="value">-</div><div class="note">Scenario label</div></div>
      <div class="stat"><div class="label">Uptime</div><div id="uptime" class="value">00:00:00</div><div class="note">Container runtime</div></div>
      <div class="stat"><div class="label">App Mode</div><div id="mode" class="value">-</div><div class="note">Environment config</div></div>
    </section>

    <main class="grid">
      <section class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">Service Status</h2>
            <p class="card-subtitle">Live status from /healthz, /ready, and /info.</p>
          </div>
          <span class="badge good" id="service-badge">Healthy</span>
        </div>
        <div class="card-body">
          <div class="probes">
            <div class="probe">
              <div class="probe-row"><span class="probe-name">Liveness</span><span id="health-badge" class="badge good">Passing</span></div>
              <div class="bar"><span id="health-bar"></span></div>
            </div>
            <div class="probe">
              <div class="probe-row"><span class="probe-name">Readiness</span><span id="ready-badge" class="badge good">Ready</span></div>
              <div class="bar"><span id="ready-bar"></span></div>
            </div>
          </div>

          <table class="details">
            <tr><th>Application</th><td>i27Academy Demo App</td></tr>
            <tr><th>Hostname</th><td id="host-full">-</td></tr>
            <tr><th>Color</th><td id="color">-</td></tr>
            <tr><th>DB_URL</th><td id="db">-</td></tr>
          </table>
        </div>
      </section>

      <section class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">Actions</h2>
            <p class="card-subtitle">Run common Kubernetes demo endpoints.</p>
          </div>
        </div>
        <div class="card-body">
          <div class="actions">
            <button class="action" onclick="callEp('/info')"><strong>Info</strong><span>/info</span></button>
            <button class="action" onclick="callEp('/healthz')"><strong>Liveness</strong><span>/healthz</span></button>
            <button class="action" onclick="callEp('/ready')"><strong>Readiness</strong><span>/ready</span></button>
            <button class="action" onclick="callEp('/slow?seconds=5')"><strong>Slow</strong><span>/slow?seconds=5</span></button>
            <button class="action warning" onclick="callEp('/toggle-health')"><strong>Toggle Health</strong><span>/toggle-health</span></button>
            <button class="action warning" onclick="callEp('/toggle-ready')"><strong>Toggle Ready</strong><span>/toggle-ready</span></button>
            <button class="action danger" onclick="callEp('/oom')"><strong>Simulate OOM</strong><span>/oom</span></button>
            <button class="action danger" onclick="callEp('/crash')"><strong>Crash App</strong><span>/crash</span></button>
          </div>
        </div>
      </section>

      <section class="card" style="grid-column: 1 / -1;">
        <div class="card-header">
          <div>
            <h2 class="card-title">Activity Log</h2>
            <p class="card-subtitle">Requests and responses from this page.</p>
          </div>
          <span class="badge good" id="feed-badge">Connected</span>
        </div>
        <div class="card-body">
          <div id="log" class="log"></div>
        </div>
      </section>
    </main>
  </div>

<script>
const logEl = document.getElementById('log');

function text(id, value) {
  document.getElementById(id).textContent = value || '-';
}

function addLog(message, type='info') {
  const row = document.createElement('div');
  row.className = 'log-entry';
  const now = new Date().toLocaleTimeString('en-GB', { hour12: false });
  row.innerHTML = `<span class="time">[${now}]</span><span class="type-${type}">[${type.toUpperCase()}]</span> ${message}`;
  logEl.appendChild(row);
  logEl.scrollTop = logEl.scrollHeight;
}

function setBadge(id, ok, goodText, badText) {
  const badge = document.getElementById(id);
  badge.className = `badge ${ok ? 'good' : 'bad'}`;
  badge.textContent = ok ? goodText : badText;
}

function setProbe(kind, ok) {
  setBadge(`${kind}-badge`, ok, kind === 'health' ? 'Passing' : 'Ready', kind === 'health' ? 'Failing' : 'Not Ready');
  const bar = document.getElementById(`${kind}-bar`);
  bar.style.width = ok ? '100%' : '18%';
  bar.style.background = ok ? 'var(--green)' : 'var(--red)';
}

function uptime(seconds) {
  const u = seconds || 0;
  const h = Math.floor(u / 3600);
  const m = Math.floor((u % 3600) / 60);
  const s = Math.floor(u % 60);
  return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
}

async function fetchStatus() {
  try {
    const res = await fetch('/info');
    const data = await res.json();
    const healthy = Boolean(data.healthy);
    const ready = Boolean(data.ready);
    const ok = healthy && ready;

    text('node', (data.hostname || 'unknown').slice(0, 14));
    text('env', data.env || 'production');
    text('version', data.version);
    text('episode', data.episode);
    text('mode', data.config.APP_MODE);
    text('uptime', uptime(data.uptime_s));
    text('host-full', data.hostname || 'unknown');
    text('color', data.color);
    text('db', data.config.DB_URL);

    document.getElementById('overall-status').textContent = ok ? 'Operational' : 'Attention';
    document.getElementById('status-dot').style.background = ok ? 'var(--green)' : 'var(--red)';

    const service = document.getElementById('service-badge');
    service.className = `badge ${ok ? 'good' : 'warn'}`;
    service.textContent = ok ? 'Healthy' : 'Needs Attention';

    setProbe('health', healthy);
    setProbe('ready', ready);
    document.getElementById('feed-badge').className = 'badge good';
    document.getElementById('feed-badge').textContent = 'Connected';
  } catch (err) {
    document.getElementById('feed-badge').className = 'badge bad';
    document.getElementById('feed-badge').textContent = 'Disconnected';
    addLog('Unable to load /info', 'error');
  }
}

async function callEp(path) {
  addLog(`GET ${path}`);
  try {
    const start = performance.now();
    const res = await fetch(path);
    const ms = Math.round(performance.now() - start);
    let body;
    try { body = await res.json(); } catch { body = await res.text(); }
    addLog(`${res.status} from ${path} in ${ms}ms`, res.ok ? 'info' : 'error');
    addLog(JSON.stringify(body), res.ok ? 'info' : 'error');
    fetchStatus();
  } catch (err) {
    addLog(`Request failed: ${err.message}`, 'error');
  }
}

fetchStatus();
setInterval(fetchStatus, 3000);
addLog('i27Academy UI ready.');
</script>
</body>
</html>"""

@app.route("/ui")
def ui():
    return render_template_string(UI_HTML)

@app.route("/")
def home():
    uptime = round(time.time() - START_TIME, 1)
    log.info(f"GET / — version={APP_VERSION}")
    return jsonify({
        "app": "i27Academy Demo App", "version": APP_VERSION,
        "env": APP_ENV, "color": APP_COLOR, "episode": EPISODE,
        "uptime_s": uptime,
        "message": f"Hello from i27Academy! Running {APP_VERSION}",
        "docs": "github.com/i27academy/devops-interview-series"
    }), 200

@app.route("/healthz")
def liveness():
    if not HEALTHY:
        log.warning("GET /healthz — FAILING")
        return jsonify({"status": "unhealthy", "version": APP_VERSION,
                        "reason": "simulated via /toggle-health"}), 500
    return jsonify({"status": "healthy", "version": APP_VERSION, "check": "liveness"}), 200

@app.route("/ready")
def readiness():
    if not READY:
        log.warning("GET /ready — NOT READY")
        return jsonify({"status": "not ready", "version": APP_VERSION,
                        "reason": "simulated via /toggle-ready"}), 503
    return jsonify({"status": "ready", "version": APP_VERSION, "check": "readiness"}), 200

@app.route("/info")
def info():
    config = {k: v for k, v in os.environ.items()
              if any(k.startswith(p) for p in
              ['DB_', 'APP_', 'EPISODE', 'CACHE_', 'API_'])}
    return jsonify({
        "app"      : "i27Academy Demo App",
        "version"  : APP_VERSION,
        "env"      : APP_ENV,
        "color"    : APP_COLOR,
        "episode"  : EPISODE,
        "hostname" : os.environ.get("HOSTNAME", "unknown"),
        "uptime_s" : round(time.time() - START_TIME, 1),
        "healthy"  : HEALTHY,
        "ready"    : READY,
        "config"   : config,
        "endpoints": {
            "/ui"            : "Dashboard UI",
            "/"              : "App home",
            "/healthz"       : "Liveness probe",
            "/ready"         : "Readiness probe",
            "/info"          : "Full app info",
            "/crash"         : "Simulate crash",
            "/oom"           : "Simulate OOMKilled",
            "/slow"          : "Simulate slow response",
            "/toggle-health" : "Toggle liveness probe",
            "/toggle-ready"  : "Toggle readiness probe",
        }
    }), 200

@app.route("/crash")
def crash():
    log.error("GET /crash — exit 1")
    sys.stdout.flush()
    os._exit(1)

@app.route("/oom")
def oom():
    log.warning("GET /oom — allocating memory")
    def eat():
        data = []
        while True:
            data.append("x" * 10 * 1024 * 1024)
            log.warning(f"Allocated {len(data)*10}MB...")
            time.sleep(0.2)
    threading.Thread(target=eat, daemon=True).start()
    return jsonify({"status": "started", "message": "OOMKill incoming",
                    "version": APP_VERSION}), 200

@app.route("/slow")
def slow():
    delay = int(request.args.get("seconds", 30))
    log.warning(f"GET /slow — sleeping {delay}s")
    time.sleep(delay)
    return jsonify({"status": "ok", "message": f"Responded after {delay}s",
                    "version": APP_VERSION}), 200

@app.route("/toggle-health")
def toggle_health():
    global HEALTHY
    HEALTHY = not HEALTHY
    state = "PASSING" if HEALTHY else "FAILING"
    log.warning(f"Liveness probe now {state}")
    return jsonify({"healthy": HEALTHY, "message": f"Liveness probe now {state}",
                    "version": APP_VERSION}), 200

@app.route("/toggle-ready")
def toggle_ready():
    global READY
    READY = not READY
    state = "READY" if READY else "NOT READY"
    log.warning(f"Readiness probe now {state}")
    return jsonify({"ready": READY, "message": f"Readiness probe now {state}",
                    "version": APP_VERSION}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    log.info("=" * 50)
    log.info("  i27Academy Demo App")
    log.info(f"  Version : {APP_VERSION}")
    log.info(f"  Episode : {EPISODE}")
    log.info(f"  UI      : http://localhost:{port}/ui")
    log.info("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=False)
