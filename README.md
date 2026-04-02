# Swiss Ephemeris API

**License**: [AGPL-3.0-or-later](LICENSE) — Source code is always public and matches the running server.

REST API for Swiss Ephemeris astronomical calculations. Built with Python 3.12+, FastAPI, and [pysweph](https://github.com/sailorfe/pysweph).

> This project uses Swiss Ephemeris by [Astrodienst AG](https://www.astro.com/swisseph/swephinfo_e.htm).
> Swiss Ephemeris is free for non-commercial use. For commercial use,
> a license must be obtained from Astrodienst AG.

**Source**: https://github.com/devtrongle/Swiss-Ephemeris-API

---

## Features

| Category | Coverage |
|---|---|
| Planets | Sun–Pluto, Chiron, Ceres, Pallas, Juno, Vesta, Earth |
| Lunar Nodes | True/Mean North & South Node |
| Lilith | True/Mean Black Moon (apogee of Moon's orbit) |
| Special Points | Part of Fortune, Vertex, Anti-Vertex |
| Fixed Stars | 35 fixed stars |
| Houses | Placidus, Koch, Whole Sign, Equal, Porphyrius, Regiomontanus, Campanus, Alcabitius, Morinus (+6 more) |
| Sidereal | 22 ayanamsa systems (Lahiri, Krishnamurti, Raman, etc.) |
| Eclipses | Solar & Lunar (past and future) |
| Lunar Phase | Phase name, illumination %, elongation, lunar age |

---

## Quick Start

### 1. Download ephemeris files

The API requires Swiss Ephemeris data files. Download from the official source (GitHub):

```bash
# Required — planet ephemeris
curl -o ephe/sepl_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1

# Required — Moon / lunar ephemeris
curl -o ephe/semo_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1

# Required — fixed star catalog (30 major stars)
curl -o ephe/seas_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
```

> **Why these three files?** `sepl_18.se1` covers all planets except the Moon (Jupiter–Pluto, DE431).
> `semo_18.se1` provides the lunar ephemeris for the Moon.
> `seas_18.se1` provides the fixed star catalog.
> All three are needed for the API to function. Without them, `/health` returns 503.
>
> **Note**: File extension is `.se1` (not `.se`). The older `.se` format was deprecated.

For extended historical calculations (before 1301 or after 1701), download the full archive
(2.4 GB, covers **13201 BC – 17191 AD**) from Dropbox:

```bash
curl -L "https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=1" -o ephe/swe_unix.tar.gz
tar -xzf ephe/swe_unix.tar.gz -C ephe/
```

For asteroid files (Chiron, Ceres, Pallas, Juno, Vesta) — download from Dropbox:

```bash
# Asteroid 1–99 (Ceres=1, Pallas=2, Juno=3, Vesta=4)
curl -L "https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=1" -o ast1.tar.gz
# Asteroid 100–9999
curl -L "https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=1" -o ast2.tar.gz
# etc.
```

> See: <https://www.astro.com/swisseph/swedownload_e.htm>

### 2. Install dependencies

```bash
pip install -e .
```

### 3. Run

```bash
EPHE_PATH=$(pwd)/ephe uvicorn app.main:app --reload
```

Or with an `.env` file:

```bash
cp .env.example .env
# edit .env if needed
uvicorn app.main:app --reload
```

### 4. Verify

```bash
curl http://localhost:8000/health
# → {"status": "ok", "ephe_path": "./ephe", "source": "..."}

curl -X POST http://localhost:8000/api/v1/planets \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": "1990-01-15T12:00:00",
    "timezone": "Asia/Ho_Chi_Minh",
    "latitude": 21.0285,
    "longitude": 105.8542,
    "ayanamsa": "LAHIRI"
  }'
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Project info & AGPL notice |
| GET | `/health` | Health check |
| POST | `/api/v1/planets` | Planet positions (15 bodies) |
| POST | `/api/v1/houses` | House cusps & ASC/MC |
| POST | `/api/v1/birth-chart` | Planets + houses combined |
| POST | `/api/v1/fixed-stars` | 30 fixed star positions |
| GET | `/api/v1/eclipses` | Solar & lunar eclipses |
| POST | `/api/v1/lunar-phase` | Phase, illumination, lunar age |
| POST | `/api/v1/lunar-nodes` | North/South nodes + Lilith |
| POST | `/api/v1/special-points` | Part of Fortune, Vertex, Anti-Vertex |

Full documentation: [docs/API.md](docs/API.md)

---

## Docker

```bash
docker compose up --build
```

The Dockerfile automatically downloads the ephemeris files from the official GitHub source.

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `EPHE_PATH` | `./ephe` | Path to directory containing `.se1` files |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `8000` | Bind port |
| `CORS_ORIGINS` | `*` | CORS allowed origins (comma-separated) |

---

## License

This program is free software: you can redistribute it and/or modify it under
the terms of the **GNU Affero General Public License** (AGPL) version 3 or later.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU AGPL for more details.

You should have received a copy of the GNU AGPL along with this program.
If not, see <https://www.gnu.org/licenses/>.

**Note**: Swiss Ephemeris data files (`.se1` files) have their own license from
Astrodienst AG. They are free for non-commercial use. For commercial use,
contact Astrodienst AG.
