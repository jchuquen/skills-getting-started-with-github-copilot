import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test.user@example.com"

    # ensure clean start for this test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    encoded_activity = urllib.parse.quote(activity, safe="")
    resp = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    assert resp.status_code == 200, resp.text
    assert email in activities[activity]["participants"]

    # Confirm via GET
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data = resp2.json()
    assert email in data[activity]["participants"]

    # Unregister
    resp3 = client.post(f"/activities/{encoded_activity}/unregister", params={"email": email})
    assert resp3.status_code == 200, resp3.text
    assert email not in activities[activity]["participants"]
