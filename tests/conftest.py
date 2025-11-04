import os
import sys
import copy
import pytest
from fastapi.testclient import TestClient

# Ensure project root is on sys.path for `import src`
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.app import app, activities as activities_store


@pytest.fixture(autouse=True)
def reset_activities():
    # Snapshot the in-memory activities and restore after each test
    # Store only the participants lists which change during tests
    snapshot = {name: act["participants"][:] for name, act in activities_store.items()}
    try:
        yield
    finally:
        # Restore only the participants lists instead of deep copying entire structure
        for name, participants in snapshot.items():
            if name in activities_store:
                activities_store[name]["participants"] = participants[:]


@pytest.fixture()
def client():
    return TestClient(app)
