import pytest
import swisseph as swe
import os


def _find_ephe_path() -> str:
    candidates = [
        os.environ.get("EPHE_PATH", ""),
        os.path.join(os.path.dirname(__file__), "..", "ephe"),
        "./ephe",
        "/Users/tronglb/Task/Velora-Workspace/swiss-ephemeris-api/ephe",
    ]
    for p in candidates:
        if p and (os.path.isdir(p) or os.path.isfile(os.path.join(p, "sepl_18.se1"))):
            return p
    return "./ephe"


@pytest.fixture(scope="session")
def ephe_path() -> str:
    """Return a valid ephe path — tries EPHE_PATH env then common locations."""
    path = _find_ephe_path()
    swe.set_ephe_path(path)
    return path


@pytest.fixture
def swiss_core(ephe_path: str):
    """Instantiate SwissEphemerisCore with a valid ephe path."""
    from app.core.swisseph_core import SwissEphemerisCore
    return SwissEphemerisCore(ephe_path=ephe_path)
