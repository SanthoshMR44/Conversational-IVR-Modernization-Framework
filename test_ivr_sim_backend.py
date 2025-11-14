# test_ivr_sim_backend.py
from fastapi.testclient import TestClient
from ivr_sim_backend import app, active_calls

client = TestClient(app)


def test_start_call():
    """Test that a call starts and returns call_id + status"""
    active_calls.clear()  # Ensure clean state
    response = client.post("/start_call", json={"caller": "+919876543210"})

    assert response.status_code == 200
    data = response.json()

    assert "call_id" in data
    assert data["status"] == "started"
    assert data["call_id"] in active_calls


def test_prompt_after_start():
    """Test that prompt returns correct welcome message"""
    active_calls.clear()

    start = client.post("/start_call", json={"caller": "9999"}).json()
    call_id = start["call_id"]

    response = client.get(f"/prompt/{call_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["prompt"] == "Welcome to the IVR system. What would you like to do?"


def test_user_input():
    """Test user input response"""
    active_calls.clear()

    start = client.post("/start_call", json={"caller": "7777"}).json()
    call_id = start["call_id"]

    response = client.post(f"/input/{call_id}", json={"user_input": "balance"})
    assert response.status_code == 200

    data = response.json()
    assert data["response"] == "You selected: balance"


def test_end_call():
    """Test ending a call removes it from active_calls"""
    active_calls.clear()

    start = client.post("/start_call", json={"caller": "555"}).json()
    call_id = start["call_id"]

    end = client.post(f"/end_call/{call_id}")
    assert end.status_code == 200
    assert end.json()["status"] == "ended"

    assert call_id not in active_calls

    # After ending, prompt should return 404
    check = client.get(f"/prompt/{call_id}")
    assert check.status_code == 404
