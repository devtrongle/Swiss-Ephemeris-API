from contextlib import asynccontextmanager

import swisseph as swe

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import __app_name__, __version__
from app.core.config import settings
from app.api.v1.router import router as v1_router
from app.deps import init_core, get_swiss_core


AGPL_NOTICE = (
    "This project is based on Swiss Ephemeris by Astrodienst AG and is released\n"
    "under the GNU Affero General Public License (AGPL-3.0-or-later).\n"
    "Source code must always be public and match the code running on this server.\n"
    "Source: https://github.com/<YOUR_USERNAME>/swiss-ephemeris-api"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: eagerly initialize SwissEphemerisCore (sets ephe_path once)
    swe.set_ephe_path(settings.ephe_path)
    init_core()
    yield
    # Shutdown: nothing to clean up (stateless)


def create_app() -> FastAPI:
    app = FastAPI(
        title=__app_name__,
        version=__version__,
        description="REST API for Swiss Ephemeris astronomical calculations. "
        "Comprehensive coverage: planets, houses, lunar nodes, fixed stars, eclipses, and lunar phases.",
        license_info={"name": "AGPL-3.0-or-later", "url": "https://www.gnu.org/licenses/agpl-3.0.html"},
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register v1 routes
    app.include_router(v1_router)

    # Root endpoint — AGPL notice
    @app.get("/", tags=["info"])
    async def root() -> dict:
        return {
            "name": __app_name__,
            "version": __version__,
            "license": "AGPL-3.0-or-later",
            "notice": AGPL_NOTICE,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    # Health check
    @app.get("/health", tags=["info"])
    async def health() -> dict:
        try:
            get_swiss_core()  # verify singleton was initialized
            return {
                "status": "ok",
                "ephe_path": settings.ephe_path,
                "source": "https://github.com/<YOUR_USERNAME>/swiss-ephemeris-api",
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Swiss Ephemeris not available: {e}")

    return app


app = create_app()
