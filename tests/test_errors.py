import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_twice_returns_400():
    activity = "Programming Class"
    email = "duplicate.test@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    encoded_activity = urllib.parse.quote(activity, safe="")

    # First signup should succeed
    resp1 = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    assert resp1.status_code == 200

    # Second signup should return 400 (already signed up)
    resp2 = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    assert resp2.status_code == 400

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)


def test_unregister_nonexistent_returns_404():
    activity = "Programming Class"
    email = "not.registered@example.com"

    # Ensure email is not in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    encoded_activity = urllib.parse.quote(activity, safe="")
    resp = client.post(f"/activities/{encoded_activity}/unregister", params={"email": email})
    assert resp.status_code == 404


def test_activity_not_found_returns_404():
    activity = "NoSuchActivity"
    email = "someone@example.com"
    encoded_activity = urllib.parse.quote(activity, safe="")

    resp_signup = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    assert resp_signup.status_code == 404

    resp_unreg = client.post(f"/activities/{encoded_activity}/unregister", params={"email": email})
    assert resp_unreg.status_code == 404
