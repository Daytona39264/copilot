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
    snapshot = copy.deepcopy(activities_store)
    try:
        yield
    finally:
        activities_store.clear()
        activities_store.update(copy.deepcopy(snapshot))


@pytest.fixture()
def client():
    return TestClient(app)
