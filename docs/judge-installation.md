# Judge installation: desktop and Android Termux

This is a **local-only** FastAPI/SQLite/MCP demo, not a public service or a native Android/Vega application. A phone browser can access the app when the server runs on that same phone. No Amazon account, paid service, or Kiro credit is required for this local demonstration.

## Required software and Python packages

- Git (for cloning), Python **3.11-3.13 recommended**, pip, and optional Node.js (for JavaScript syntax verification).
- `requirements.txt` installs **FastAPI**, **Uvicorn**, **HTTPX** (FastAPI TestClient), **Starlette**, and **Pydantic**. Their dependency trees are installed automatically by pip, including packages such as `pydantic-core` (Pydantic v2), `anyio`, `click`, `h11`, `typing-extensions`, and others as required by the resolved versions. Python stdlib provides SQLite, unittest, CSV, and other modules; no extra SQLite Python package is needed.
- Confirm the install with `python -m pip check` and `python -c "import fastapi, uvicorn, httpx, starlette, pydantic; print('Dependencies OK')"`.

## Desktop Linux / macOS (recommended reproducible judge path)

```sh
git clone https://github.com/interplanetarysister/AmazonHackathon.git
cd AmazonHackathon
git switch integration/judge-ready-20261020
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m unittest discover -s tests -v
python scripts/smoke_mcp.py
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 on the same computer. When the integration branch is verified and merged to main, judges should omit the `git switch` command.

## Android phone with native Termux (optional)

On an Android device using Termux, install platform dependencies and clone first:

```sh
pkg update -y
pkg install python git -y
cd ~
git clone https://github.com/interplanetarysister/AmazonHackathon.git
cd AmazonHackathon
git switch integration/judge-ready-20261020
python --version
```

**Compatibility warning:** Current native Termux may ship Python 3.14. The project owner encountered `maturin`/`pydantic-core` failures on this Python version, and no `python-pydantic` package was available in their configured Termux mirror. Installing individual dependencies with `--no-deps` left FastAPI broken; this is not a reliable workaround. Do **not** claim this setup passes or repeatedly retry the same failing build. A Python 3.11–3.13 Linux environment is the preferred fallback; Termux can run a supported Ubuntu container via `proot-distro` where an appropriate Python version is available. Native Termux is conditional on compatible wheels/build tools becoming available.

When your Python version and build environment support Pydantic, continue:

```sh
python -m pip install -r requirements.txt
python -m pip check
python -c "import fastapi, uvicorn, httpx, starlette, pydantic; print('Dependencies OK')"
python -m unittest discover -s tests -v
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 in the browser on the **same Android phone** while the Termux server is running.

### If Termux cannot build Pydantic

Do not continue with a broken partial installation. A supported Linux Python environment can be installed without touching the existing Termux files:

```sh
pkg install proot-distro -y
proot-distro install ubuntu
proot-distro login ubuntu
apt update
apt install -y python3 python3-venv python3-pip git
python3 --version
```

If `python3 --version` reports a supported version (recommended 3.11–3.13), clone the repo **inside that Ubuntu shell** and follow the desktop steps using `python3`. If Ubuntu provides Python 3.14 instead, do not assume the workaround fixes the issue; use a compatible desktop or explicitly provision a supported Python version. Do not run Termux `pkg` inside Ubuntu. These are instructions, not a recorded successful clean install.

## Tests, optional tooling and release checks

- `python -m unittest discover -s tests -v`: backend + five simulated package scenarios + MCP endpoint tests
- `python scripts/smoke_mcp.py`: live local MCP smoke test
- `python scripts/verify_client.py`: JavaScript syntax check; requires **Node.js**; missing Node returns a nonzero `NOT VERIFIED`, not a successful skip
- `python -m pip check`: reports incompatible or missing installed dependencies

The app stores local demo records in SQLite and has **no authenticated user separation**. Do not bind `0.0.0.0` or expose a public deployment. Sample carrier, Ring-formatted and synthetic logistics evidence are not authentic third-party records. Real Ring or Vega OS eligibility requires separate proof.

Current status: instructions committed; clean-room runs, test pass, and mobile success on a supported environment must still be independently confirmed.
