# Electricity Tracker

Small Python project that fetches electricity price and consumption data and exposes a small Flask API.

Prerequisites
- Python 3.8+ (this project used Python 3.9 in the venv)

Quick setup

1. Create and activate virtual environment (macOS / zsh):

```bash
cd /Users/kotimac/Documents/Work/eletrack/electricity-tracker-main
python3 -m venv .venv
source .venv/bin/activate
```

2. Install requirements:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Running the server

```bash
# inside the activated venv
python ele_server.py
```

Common commands

- Run the CLI main script:

```bash
python ele_main.py --date now
```

- Run a quick smoke test (in another terminal):

```bash
curl -sS http://127.0.0.1:5000/data/now
```

Notes

- `requirements.txt` includes `XlsxWriter` (used by `ele_parser.py`).
- Environment variables (optional for some endpoints) can be set in a `.env` file: `FORTUM_TOKEN`, `FORTUM_CUSTOMER_ID`, `DATAHUB_TOKEN`, `DATAHUB_METERING_POINT_EAN`, etc.
- If you encounter TLS/OpenSSL warnings during install, it is generally safe for local development. If you need production-grade TLS, consider using a Python build linked to a modern OpenSSL.
